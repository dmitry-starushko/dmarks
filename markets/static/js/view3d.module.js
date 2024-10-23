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
    constructor(parent_id, gltf_url, outlets_url, paint_map, ground_color, decoration_color, decoration_opacity) {
        const v3d = document.getElementById(parent_id);
        const width = v3d.clientWidth;
        const height = v3d.clientHeight;
        this._width = width; // TODO resize handler
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
                    const gb = ground.geometry.boundingBox; // -- ground bounding box
                    const gc = new THREE.Vector3(); // -- ground center
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
                    this._pointer = new THREE.Vector2();
                    this._targets = new Array();

                    const renderer = new THREE.WebGLRenderer({ antialias: true }); // -- camera positioning, renderer
                    this._renderer = renderer;
                    renderer.shadowMap.enabled = true;
                    renderer.setSize(width, height);
                    this.__setup_raycasting__();
                    v3d.appendChild(renderer.domElement);

                    const controls = new OrbitControls(camera, renderer.domElement); // -- controls
                    this._controls = controls;
                    this.__reset_look_position__();

                    renderer.setAnimationLoop(time => this.__render_loop__(time));
                    const outlets = await (await fetch(outlets_url)).json(); // -- paint scene
                    this.__prepare_scene__(outlets, paint_map, decoration_color, decoration_opacity);
                    ground.material.color = new THREE.Color(ground_color);
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
//            console.log(pointed[0].object.parent.name);
            pointed[0].object.parent.children.forEach(mesh => {
                mesh.material.emissive.setHex(def_emissive_color);
                mesh.material.emissiveIntensity = def_emissive_intensity;
            });
        }
        this._renderer.render(this._scene, this._camera);
    }

    __setup_raycasting__() {
        this._renderer.domElement.addEventListener("pointermove", event => {
            const mx = event.offsetX;
            const my = event.offsetY;
            this._pointer.set(2.0 * mx / this._width - 1.0, -2.0 * my / this._height + 1.0);
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
                this._targets.push(obj);
                obj.children.forEach((mesh, index) => {
                    const geometry = new THREE.EdgesGeometry(mesh.geometry);
                    const material = new THREE.LineBasicMaterial({ color: "black" });
                    const wireframe = new THREE.LineSegments(geometry, material);
                    this._scene.add(wireframe);
                });
                if(obj.userData.id in outlets) {
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
}

export { View3D };