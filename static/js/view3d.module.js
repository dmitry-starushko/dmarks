import * as THREE from "three";
import { GLTFLoader } from "gltf_loader";
import { OrbitControls } from "orbit_controls";
import { MapControls } from "map_controls";

const def_camera_height = 75.0;
const def_camera_fov = 60.0;
const def_camera_near = 0.01;
const def_camera_far = 10000.0;
const def_orb_tgt_height = -10.0;
const def_scene_background_color = 0x11aabb;
const def_outlet_metallness = 0.55;
const def_decoration_metallness = 0.25;
const def_emissive_color = 0xffffff;
const def_emissive_intensity = 0.7;
const def_fog_density = 0.001;
const def_marker_color = 0xf46b12;
const def_marker_metalness = 0.75;
const def_marker_vdist = 1.0;

class View3D {
    constructor(parent_id,
                urls_url,
                scheme_pk,
                legend,
                ground_color,
                decoration_color,
                decoration_opacity,
                listener) {
        const parent = document.getElementById(parent_id);
        if(!parent) { throw `DOM element with id <${parent_id}> not found`; }
        const width = parent.clientWidth;
        const height = parent.clientHeight;
        this._urls_url = urls_url,
        this._parent = parent;
        this._listener = listener ? listener : parent;
        this._width = width;
        this._height = height;
        this._ground_color = ground_color;
        this._decoration_color = decoration_color;
        this._decoration_opacity = decoration_opacity;
        this._events_actl = new AbortController();
        this._csrf_token = Cookies.get('csrftoken');
        this.__load_scene__(scheme_pk, legend);
    }

    async __load_scene__(scheme_pk, legend) {
        this._scheme_pk = scheme_pk;
        this._legend = legend;
        await this.__take_urls__();

        const loader = new GLTFLoader();
        loader.load(
            this._urls.url_scheme_gltf,
            async gltf => {
                const scene = new THREE.Scene();
                scene.add(gltf.scene);
                scene.background = new THREE.Color(def_scene_background_color);
                if(def_fog_density > 0.0) { scene.fog = new THREE.FogExp2(this._ground_color, def_fog_density); }
                this._scene = scene;

                const camera = new THREE.PerspectiveCamera(def_camera_fov, this._width / this._height, def_camera_near, def_camera_far);
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
                    this._targets = [];

                    this.__create_marker__();
                    const _listener = this._listener;
                    const _pointed_marker_position = this._pointed_marker_position;
                    this._cursor = {
                        _listener: _listener,
                        _id_point: null,
                        _id_down: null,
                        _ch_count: 0,

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
                            if(this._id_down === value && this._ch_count > 0) {
                                window.setTimeout(() => { this._listener.dispatchEvent(new CustomEvent("outlet_clicked", { detail: {
                                    id: value,
                                    marker: {
                                        x: _pointed_marker_position.x,
                                        y: _pointed_marker_position.y,
                                        z: _pointed_marker_position.z
                                    }
                                }})); });
                            }
                        }
                    };

                    const renderer = new THREE.WebGLRenderer({ antialias: true }); // -- camera positioning, renderer
                    this._renderer = renderer;
                    renderer.shadowMap.enabled = true;
                    renderer.setSize(this._width, this._height);
                    this.__setup_events__();
                    this._parent.appendChild(renderer.domElement);

                    const orb_controls = new OrbitControls(camera, renderer.domElement); // -- controls
                    orb_controls.enableDamping = true; // an animation loop is required when either damping or auto-rotation are enabled
                    orb_controls.dampingFactor = 0.15;
                    orb_controls.screenSpacePanning = false;
                    orb_controls.maxPolarAngle = Math.PI / 2.0;
                    orb_controls.enabled = false;

                    const map_controls = new OrbitControls(camera, renderer.domElement); // -- controls
                    map_controls.enableDamping = true; // an animation loop is required when either damping or auto-rotation are enabled
                    map_controls.dampingFactor = 0.15;
                    map_controls.screenSpacePanning = false;
                    map_controls.enableRotate = false;
                    map_controls.mouseButtons = {
                        LEFT: THREE.MOUSE.PAN,
                        MIDDLE: THREE.MOUSE.DOLLY,
                        RIGHT: THREE.MOUSE.ROTATE
                    }
                    map_controls.enabled = false;
                    this._avail_controls = [orb_controls, map_controls];
                    for (const c of this._avail_controls) {
                        c.addEventListener('start', ()=>{ this._cursor._ch_count = 10; });
                        c.addEventListener('change', ()=>{ this._cursor._ch_count--; });
                        c.addEventListener('end', ()=>{ });
                    }
                    this._controls = orb_controls;
                    this.__reset_look_position__();

                    renderer.setAnimationLoop(time => this.__render_loop__(time)); // -- start render
                    const outlets = await (await fetch(this._urls.url_scheme_outlets_state)).json(); // -- paint scene
                    ground.material.color = new THREE.Color(this._ground_color);
                    await this.__take_paint_map__();
                    this.__build_outlet_edges__();
                    this.__paint_outlets__(outlets);
                    this.__create_labels__();

                    const resize_observer  = new ResizeObserver(() => { this.__on_resize__(); });
                    resize_observer.observe(this._parent);
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
                alert(`Ошибка при создании сцены:\n${await(await fetch(urls_url)).text()}`);
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
                const bb = mesh.geometry.boundingBox;
                bb.getCenter(this._pointed_marker_position);
                this._pointed_marker_position.y = bb.max.y + def_marker_vdist;
            });
        } else {
            this._cursor.id_point = null;
        }
        if(this._marker.visible) {
            const f = 0.35;
            this._marker.rotation.y = time / 300.0;
            this._marker.position.set(
                this._marker.position.x * (1-f) + this._target_marker_position.x * f,
                this._marker.position.y * (1-f) + this._target_marker_position.y * f + 0.25 * Math.cos(time / 91.0),
                this._marker.position.z * (1-f) + this._target_marker_position.z * f
            );
        }
        this._renderer.render(this._scene, this._camera);
    }

    __setup_events__() {
        this._events_actl.abort();
        this._events_actl = new AbortController();
        const opt = { signal: this._events_actl.signal };
        const dom_element = this._renderer.domElement;
        dom_element.addEventListener("pointermove", event => {
            const mx = event.offsetX;
            const my = event.offsetY;
            this._pointer.set(2.0 * mx / this._width - 1.0, -2.0 * my / this._height + 1.0);
        }, opt);
        dom_element.addEventListener("mousedown", event => {
            this._cursor.id_down = this._cursor.id_point;
        }, opt);
        dom_element.addEventListener("click", event => {
            this._cursor.id_click = this._cursor.id_point;
        }, opt);
        this._listener.addEventListener("outlet_clicked", event => {
            let found = false;
            if ("marker" in event.detail) { // -- event from myself
                const marker = event.detail.marker;
                this._target_marker_position.set(marker.x, marker.y, marker.z);
                found = !!event.detail.id;
            } else { // -- external event
                if(event.detail.id) {
                    for(const obj of this._targets) {
                        if(obj.userData.id === event.detail.id) {
                            obj.children.forEach(mesh => {
                                const bb = mesh.geometry.boundingBox;
                                bb.getCenter(this._target_marker_position);
                                this._target_marker_position.y = bb.max.y + def_marker_vdist;
                            });
                            found = true;
                            break;
                        }
                    }
                }
            }
            this._marker.visible = found;
        }, opt);
        this._listener.addEventListener("market_storey_changed", event => {
            window.setTimeout(() => {
                this.__clear__();
                this.__load_scene__(event.detail.scheme_pk, this._legend);
            });
        }, opt);
        this._listener.addEventListener("toggle_3d_view", event => {
            window.setTimeout(() => {
                this.__toggle_controls__();
            });
        }, opt);
        this._listener.addEventListener("reset_3d_view", event => {
            window.setTimeout(() => {
                this.__reset_look_position__();
            });
        }, opt);
        this._listener.addEventListener("apply_outlet_filters", event => {
            window.setTimeout(async () => {
                const outlets = await (await fetch(
                    this._urls.url_scheme_outlets_state, {
                        method: "POST",
                        headers: {
                            'Accept': 'application/json',
                            'Content-Type': 'application/json',
                            'X-CSRFToken': this._csrf_token,
                        },
                        body: JSON.stringify(this._filters = (event.detail.filters || {}))
                    }
                )).json();
                this.__paint_outlets__(outlets);
            });
        }, opt);
        this._listener.addEventListener("next_legend", async event => {
            this._legend++;
            await this.__take_urls__();
            await this.__take_paint_map__();
            window.setTimeout(async () => {
                const outlets = await (await fetch(
                    this._urls.url_scheme_outlets_state, {
                        method: "POST",
                        headers: {
                            'Accept': 'application/json',
                            'Content-Type': 'application/json',
                            'X-CSRFToken': this._csrf_token,
                        },
                        body: JSON.stringify(this._filters || {})
                    }
                )).json();
                this.__paint_outlets__(outlets);
            });
        }, opt);
    }

    __reset_look_position__() {
        const gb = this._ground_box;
        const gc = this._ground_center;
        const n = this._avail_controls.indexOf(this._controls);
        if(n) { // Map
            const gsz = new THREE.Vector3();
            const ang = this._camera.fov * Math.PI / 360.0;
            this._ground_box.getSize(gsz);
            this._camera.position.set(gc.x, gsz.z ? 0.55 * gsz.z / Math.tan(ang) : def_camera_height, gc.z);
            this._controls.target.set(gc.x, def_orb_tgt_height, gc.z);
        } else { // Orbit
            this._camera.position.set(gb.min.x, def_camera_height, gb.min.z);
            this._controls.target.set(gc.x, def_orb_tgt_height, gc.z);
        }
        this._controls.enabled = true;
    }

    __toggle_controls__() {
        for(const c of this._avail_controls) {
            c.enabled = false;
        }
        let n = (this._avail_controls.indexOf(this._controls) + 1) % this._avail_controls.length;
        this._controls = this._avail_controls[n];
        this.__reset_look_position__();
    }

    __build_outlet_edges__() {
        this._scene.traverse(obj => {
            if((obj instanceof THREE.Group) && 'name' in obj.userData && obj.userData.name == "outlet") {
                obj.children.forEach((mesh, index) => {
                    const geometry = new THREE.EdgesGeometry(mesh.geometry, 30);
                    const material = new THREE.LineBasicMaterial({ color: "black" });
                    const wireframe = new THREE.LineSegments(geometry, material);
                    this._scene.add(wireframe);
                });
            }
        });
    }

    __paint_outlets__(outlets) {
        let paint_deco = true;
        this._targets = []
        this._scene.traverse(obj => {
            if((obj instanceof THREE.Group) && 'name' in obj.userData && obj.userData.name == "outlet") {
                if(obj.userData.id in outlets) {
                    this._targets.push(obj);
                    const paint_info = this._paint_map.get(outlets[obj.userData.id]);
                    if(paint_info) {
                        obj.children.forEach((mesh, index) => {
                            mesh.material.color.setHex(index? paint_info.roof_color : paint_info.wall_color);
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
                obj.material.color = new THREE.Color(this._decoration_color);
                obj.material.metalness = def_decoration_metallness;
                obj.material.opacity = this._decoration_opacity;
                obj.material.transparent = this._decoration_opacity < 1.0;
                paint_deco = false;
            }
        });
    }

    __create_labels__() {
        if('labels' in this._scene.children[0].userData) {
            const fs = 150;
            const canvas = document.createElement('canvas');
            let context = canvas.getContext('2d');
            context.fillStyle = '#ff0000';
            context.textAlign = 'center';
            context.font = `${fs}px serif`;

            for(const r of this._scene.children[0].userData.labels) {
                console.log(r.x, r.y, r.text);
                const tm = context.measureText(r.text);
                console.log(tm.width);
                const cnv = document.createElement('canvas');
                cnv.width = tm.width * 1.4;
                cnv.height = fs * 1.4;
                let ctx = cnv.getContext('2d');
                ctx.textAlign = context.textAlign;
                ctx.font = context.font;

                ctx.fillStyle = '#ffffff';
                ctx.fillRect(0, 0, cnv.width, cnv.height);
                ctx.fillStyle = '#0000ff';
                ctx.fillText(r.text, tm.width * 0.7, fs * 1.0);
                ctx.lineWidth = 10;
                ctx.strokeStyle = '#0000ff';
                ctx.strokeRect(1, 1, cnv.width-2, cnv.height-2);

                const tex = new THREE.CanvasTexture(cnv);
                const mat = new THREE.SpriteMaterial({map: tex, transparent: false, color: 0xffffff});
                const spr = new THREE.Sprite(mat);
                spr.scale.set(tm.width / fs, 1.0, 1.0);
                spr.position.set(r.x, 14.0, r.y);
                this._scene.add(spr);

                const material = new THREE.LineBasicMaterial({color: 0xffffff});
                const points = [];
                points.push( new THREE.Vector3(r.x, 0, r.y));
                points.push( new THREE.Vector3(r.x, 14, r.y) );
                const geometry = new THREE.BufferGeometry().setFromPoints(points);
                const line = new THREE.Line( geometry, material );
                this._scene.add( line );
            }
        }
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

    __clear__() {
        try {
            this._parent.removeChild(this._renderer.domElement);
            this._renderer.dispose();
        } catch { }
    }

    __create_marker__() {
        const length = 6, width = 3;
        const shape = new THREE.Shape();
        shape.moveTo( 0,0 );
        shape.lineTo( width, length  );
        shape.lineTo( 0, 2*length/3 );
        shape.lineTo( -width, length  );
        shape.lineTo( 0, 0 );

        const extrudeSettings = {
            steps: 2,
            depth: 0.25,
            bevelEnabled: true,
            bevelThickness: 0.1,
            bevelSize: 0.1,
            bevelOffset: 0,
            bevelSegments: 3
        };

        const geometry = new THREE.ExtrudeGeometry(shape, extrudeSettings);
        const material = new THREE.MeshStandardMaterial({ color: def_marker_color, side: THREE.DoubleSide, metalness: def_marker_metalness });
        const mesh = new THREE.Mesh(geometry, material);
        mesh.visible = false;
        mesh.position.set(this._ground_center.x, 1000, this._ground_center.z);
        this._scene.add(mesh);
        this._marker = mesh;
        this._pointed_marker_position = new THREE.Vector3();
        this._target_marker_position = new THREE.Vector3();
    }

    async __take_urls__() {
        this._urls = await (await fetch(
            this._urls_url, {
                method: "POST",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this._csrf_token,
                },
                body: JSON.stringify({
                    scheme_pk: this._scheme_pk,
                    legend: this._legend
                })
            }
        )).json();
    }

    async __take_paint_map__() {
        const legend = await (await fetch(this._urls.url_legend)).json();
        this._paint_map = new Map();
        for(const item of legend.legend) {
            this._paint_map.set(item.id, {
                wall_color: item.wall_color,
                roof_color: item.roof_color
            });
        }
    }
}

export { View3D };