import * as THREE from "three";
import { GLTFLoader } from "gltf_loader";
import { OrbitControls } from "orbit_controls";

class View3D {
    constructor(parent_id, gltf_url, outlets_url, paint_map, ground_color, decoration_color, decoration_opacity) {
        const v3d = document.getElementById(parent_id);
        const width = v3d.clientWidth, height = v3d.clientHeight;
        const camera = new THREE.PerspectiveCamera(70, width / height, 0.01, 10000);
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x11aabb)
        const loader = new GLTFLoader();
        loader.load(
            gltf_url,
            async gltf => {
                scene.add(gltf.scene);
                const ground = scene.getObjectByName("ground");
                if(ground && (ground instanceof THREE.Mesh)) {
                    ground.material.color = new THREE.Color(ground_color);
                    const bbx_min = ground.geometry.boundingBox.min;
                    const bbx_max = ground.geometry.boundingBox.max;
                    const gcx = 0.5 * (bbx_min.x + bbx_max.x);
                    const gcz = 0.5 * (bbx_min.z + bbx_max.z);
                    const ab_light = new THREE.AmbientLight(0xffffff);
                    scene.add(ab_light);
                    const dir_light = new THREE.DirectionalLight(0xffffff, 10);
                    let dir_light_t = new THREE.Object3D();
                    dir_light_t.position.set(dir_light.position.x+1,0,dir_light.position.z+1);
                    scene.add(dir_light_t);
                    dir_light.target = dir_light_t;
                    scene.add(dir_light);
                    camera.position.set(gcx, 20.0, gcz);
                    const renderer = new THREE.WebGLRenderer({ antialias: true });
                    const controls = new OrbitControls(camera, renderer.domElement);
                    controls.target = new THREE.Vector3(gcx, -10.0, gcz);

                    renderer.shadowMap.enabled = true;
                    renderer.setSize(width, height);
                    renderer.setAnimationLoop(time => {
                        controls.update();
                        renderer.render(scene, camera);
                    });
                    v3d.appendChild(renderer.domElement);

                    const outlets = await (await fetch(outlets_url)).json();

                    this.__paint_scene__(scene, outlets, paint_map, decoration_color, decoration_opacity);
                } else {
                    const msg = "Неизвестная структура сцены";
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

    __paint_scene__(scene, outlets, paint_map, decoration_color, decoration_opacity) {
        let paint_deco = true;
        scene.traverse(obj => {
            if((obj instanceof THREE.Group) && 'name' in obj.userData && obj.userData.name == "outlet") {
                obj.children.forEach((mesh, index) => {
                    const geometry = new THREE.EdgesGeometry(mesh.geometry);
                    const material = new THREE.LineBasicMaterial({ color: "black" });
                    const wireframe = new THREE.LineSegments(geometry, material);
                    scene.add( wireframe );
                });
                if(obj.userData.id in outlets) {
                    const paint_info = paint_map.get(outlets[obj.userData.id]);
                    if(paint_info) {
                        obj.children.forEach((mesh, index) => {
                            mesh.material.color = new THREE.Color(index? paint_info.roof_color : paint_info.wall_color);
                            mesh.material.metalness = 0.5;
                        });
                    } else console.error(`Вариант раскраски ТМ для состояния #${outlets[obj.userData.id]} не определён`);
                } else {
                    console.error(`Состояние ТМ #${obj.userData.id} неизвестно`);
                    obj.children.forEach((mesh, index) => {
                        mesh.material.color = new THREE.Color('gray');
                    });
                }
            }
            if(paint_deco && (obj instanceof THREE.Mesh) && obj.material.name == "decoration_material") {
                obj.material.color = new THREE.Color(decoration_color);
                obj.material.metalness = 0.25
                obj.material.opacity = decoration_opacity;
                obj.material.transparent = decoration_opacity < 1.0;
                paint_deco = false;
            }
        });
    }
}

export { View3D };