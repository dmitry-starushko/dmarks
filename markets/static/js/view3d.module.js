import * as THREE from "three";
import {GLTFLoader} from "gltf_loader";

class View3D {
    constructor(parent_id, gltf_url, paint_map) {
        const v3d = document.getElementById(parent_id);
        const width = v3d.clientWidth, height = v3d.clientHeight;
        const camera = new THREE.PerspectiveCamera(50, width / height, 0.01, 10000);
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x11aabb)
        const loader = new GLTFLoader();
        loader.load(
            gltf_url,
            async gltf => {
                scene.add(gltf.scene);
                const ground = gltf.scene.getObjectByName("ground");
                if(ground && (ground instanceof THREE.Mesh)) {
                    const bbx_min = ground.geometry.boundingBox.min;
                    const bbx_max = ground.geometry.boundingBox.max;
                    const gcx = 0.5 * (bbx_min.x + bbx_max.x);
                    const gcz = 0.5 * (bbx_min.z + bbx_max.z);
                    const ab_light = new THREE.AmbientLight(0xffffff);
                    scene.add(ab_light);
                    const dir_light = new THREE.DirectionalLight( 0xffffff, 10 );
                    let dir_light_t = new THREE.Object3D();
                    dir_light_t.position.set(dir_light.position.x+1,0,dir_light.position.z+1);
                    scene.add(dir_light_t);
                    dir_light.target = dir_light_t;
                    scene.add(dir_light);
                    camera.position.set(gcx, 20.0, gcz);
                    this.__init_scene__(scene, paint_map);

                    const renderer = new THREE.WebGLRenderer({ antialias: true });
                    renderer.shadowMap.enabled = true;
                    renderer.setSize(width, height);
                    renderer.setAnimationLoop(time => {
                        camera.rotation.y = time / 4000;
                        renderer.render(scene, camera);
                    });
                    v3d.appendChild(renderer.domElement);
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

    __init_scene__(scene, paint_map) {
        alert(paint_map.get(1).title);
        scene.traverse(obj => {
            if((obj instanceof THREE.Group) && 'name' in obj.userData && obj.userData.name == "outlet") {
                console.log(`found outlet: ${obj.userData.id}`);
                obj.children.forEach((mesh, index) => {mesh.material = this.__clone_material__(mesh.material, new THREE.Color(index? "green" : "green"));});
            }
        });
    }

    __clone_material__(material, color) {
        const new_material = Object.create(material);
        if(color) { new_material.color = color; }
        return new_material;
    }
}

export { View3D };