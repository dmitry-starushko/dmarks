import * as THREE from "three";
import { GLTFLoader } from "gltf_loader";
import { OrbitControls } from "orbit_controls";

const def_camera_height = 75.0;
const def_camera_fov = 60.0;
const def_camera_near = 0.01;
const def_camera_far = 10000.0;
const def_orb_tgt_height = -10.0;
const def_scene_background_color = 0x11aabb;
const def_outlet_metallness = 0.5;
const def_decoration_metallness = 0.25;
const def_emissive_color = 0xffffff;
const def_emissive_intensity = 0.7;

class View3D {
    constructor(parent_id,
                gltf_url,
                outlets_url,
                paint_map,
                ground_color,
                decoration_color,
                decoration_opacity,
                listener) {
        const parent = document.getElementById(parent_id);
        if(!parent) { throw `DOM element with id <${parent_id}> not found`; }
        this._parent = parent;

        const width = parent.clientWidth;
        const height = parent.clientHeight;
        this._width = width;
        this._height = height;

        const loader = new GLTFLoader();
        loader.load(
            gltf_url,
            async gltf => {
                const scene = new THREE.Scene();
                this._scene = scene;
                scene.background = new THREE.Color(def_scene_background_color);
                scene.add(gltf.scene);

                const camera = new THREE.PerspectiveCamera(def_camera_fov, width / height, def_camera_near, def_camera_far);
                this._camera = camera;

                const ground = scene.getObjectByName("ground");
                if(ground && (ground instanceof THREE.Mesh)) {
                    const gb = ground.geometry.boundingBox; // -- ground params
                    const gc = new THREE.Vector3();
                    gb.getCenter(gc);
                    this._ground_box = gb;
                    this._ground_center = gc;

                    const ab_light = new THREE.AmbientLight(0xffffff); // -- ambient light
                    scene.add(ab_light);

                    const dir_light = new THREE.DirectionalLight(0xffffff, 10); // -- directional light
                    let dir_light_t = new THREE.Object3D();
                    dir_light_t.position.set(dir_light.position.x + 1.0, 0.0, dir_light.position.z + 1.0);
                    scene.add(dir_light_t);
                    dir_light.target = dir_light_t;
                    scene.add(dir_light);

                    const raycaster = new THREE.Raycaster();
                    this._raycaster = raycaster;
                    this._pointer = new THREE.Vector2(-1.0, -1.0);
                    this._targets = new Array();
                    this._cursor = {
                        _listener: listener ? listener : parent,
                        _id_point: null,
                        _id_down: null,
                        get id_point() { return this._id_point; },
                        set id_point(value) {
                            if(this._id_point !== value) {
                                this._id_point = value;
                                window.setTimeout(() => { this._listener.dispatchEvent(new CustomEvent("outlet_pointed", { detail: { id: value } })); });
                            }
                        },
                        get id_down() { return this._id_down; },
                        set id_down(value) {
                            if(this._id_down !== value) {
                                this._id_down = value;
                            }
                        },
                        set id_click(value) {
                            if(this._id_down === value) {
                                window.setTimeout(() => { this._listener.dispatchEvent(new CustomEvent("outlet_clicked", { detail: { id: value } })); });
                            }
                        }
                    };

                    const renderer = new THREE.WebGLRenderer({ antialias: true }); // -- camera positioning, renderer
                    this._renderer = renderer;
                    renderer.shadowMap.enabled = true;
                    renderer.setSize(width, height);
                    this.__setup_raycasting__();
                    parent.appendChild(renderer.domElement);

                    const controls = new OrbitControls(camera, renderer.domElement); // -- controls
                    controls.enableDamping = true; // an animation loop is required when either damping or auto-rotation are enabled
                    controls.dampingFactor = 0.15;
                    controls.screenSpacePanning = false;
                    controls.maxPolarAngle = Math.PI / 2.0;
                    this._controls = controls;
                    this.__reset_look_position__();

                    renderer.setAnimationLoop(time => this.__render_loop__(time)); // -- start render
                    const outlets = await (await fetch(outlets_url)).json(); // -- paint scene
                    this.__prepare_scene__(outlets, paint_map, decoration_color, decoration_opacity);
                    ground.material.color = new THREE.Color(ground_color);

                    const resize_observer  = new ResizeObserver(_ => { this.__on_resize__(); });
                    resize_observer.observe(parent);
                    this._resize_observer = resize_observer;
                } else {
                    const msg = "Неверная структура сцены";
                    console.error(msg);
                    alert(msg);
                }
            },
            async progress => {
                console.log(`Progress: ${(progress.loaded / progress.total) * 100}%`);
            },
            async error => {
                console.error(error);
                alert(`Ошибка при создании сцены:\n${await(await fetch(gltf_url)).text()}`);
            }
        );
    }

    __render_loop__(time) {
        this._controls.update();
        this._raycaster.setFromCamera(this._pointer, this._camera);
        for(const tgt of this._targets) {
            tgt.children.forEach(mesh => {
                mesh.material.emissive.setHex(0);
            });
        }
        const pointed = this._raycaster.intersectObjects(this._targets);
        if(pointed.length) {
            this._cursor.id_point = pointed[0].object.parent.userData.id;
            pointed[0].object.parent.children.forEach(mesh => {
                mesh.material.emissive.setHex(def_emissive_color);
                mesh.material.emissiveIntensity = def_emissive_intensity;
            });
        } else {
            this._cursor.id_point = null;
        }
        this._renderer.render(this._scene, this._camera);
    }

    __setup_raycasting__() {
        const dom_element = this._renderer.domElement;
        dom_element.addEventListener("pointermove", event => {
            const mx = event.offsetX;
            const my = event.offsetY;
            this._pointer.set(2.0 * mx / this._width - 1.0, -2.0 * my / this._height + 1.0);
        });
        dom_element.addEventListener("mousedown", event => {
            this._cursor.id_down = this._cursor.id_point;
        });
        dom_element.addEventListener("click", event => {
            this._cursor.id_click = this._cursor.id_point;
        });
    }

    __reset_look_position__() {
        const gb = this._ground_box;
        const gc = this._ground_center;
        this._camera.position.set(gb.min.x, def_camera_height, gb.min.z);
        this._controls.target.set(gc.x, def_orb_tgt_height, gc.z);
    }

    __prepare_scene__(outlets, paint_map, decoration_color, decoration_opacity) {
        let paint_deco = true;
        this._scene.traverse(obj => {
            if((obj instanceof THREE.Group) && 'name' in obj.userData && obj.userData.name == "outlet") {
                obj.children.forEach((mesh, index) => {
                    const geometry = new THREE.EdgesGeometry(mesh.geometry);
                    const material = new THREE.LineBasicMaterial({ color: "black" });
                    const wireframe = new THREE.LineSegments(geometry, material);
                    this._scene.add(wireframe);
                });
                if(obj.userData.id in outlets) {
                    this._targets.push(obj);
                    const paint_info = paint_map.get(outlets[obj.userData.id]);
                    if(paint_info) {
                        obj.children.forEach((mesh, index) => {
                            mesh.material.color.setHex(index? paint_info.roof_color : paint_info.wall_color); //= new THREE.Color(index? paint_info.roof_color : paint_info.wall_color);
                            mesh.material.metalness = def_outlet_metallness;
                        });
                    } else console.error(`Вариант раскраски ТМ для состояния #${outlets[obj.userData.id]} не определён`);
                } else {
                    console.error(`Состояние ТМ #${obj.userData.id} неизвестно`);
                    obj.children.forEach((mesh, index) => {
                        mesh.material.color = new THREE.Color('gray');
                        mesh.material.metalness = def_outlet_metallness;
                    });
                }
            }
            if(paint_deco && (obj instanceof THREE.Mesh) && obj.material.name == "decoration_material") {
                obj.material.color = new THREE.Color(decoration_color);
                obj.material.metalness = def_decoration_metallness;
                obj.material.opacity = decoration_opacity;
                obj.material.transparent = decoration_opacity < 1.0;
                paint_deco = false;
            }
        });
    }

    __on_resize__() {
        const width = this._parent.clientWidth;
        const height = this._parent.clientHeight;
        if(width != this._width || height != this._height) {
            this._width = width;
            this._height = height;
            this._camera.aspect = width / height;
            this._camera.updateProjectionMatrix();
            this._renderer.setSize(width, height);
        }
    }
}

export { View3D };