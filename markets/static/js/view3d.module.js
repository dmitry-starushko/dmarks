import * as THREE from "three";
import {GLTFLoader} from "gltf_loader";

class View3D {
    constructor(parent_id, gltf_url) {
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
        //            const ab_light = new THREE.AmbientLight(0xffffffff);
        //            scene.add(ab_light);
                    const dir_light = new THREE.DirectionalLight( 0xffffff, 10 );
                    let dir_light_t = new THREE.Object3D();
                    dir_light_t.position.set(dir_light.position.x+1,0,dir_light.position.z+1);
                    scene.add(dir_light_t);
                    dir_light.target = dir_light_t;
                    scene.add(dir_light);
                    camera.position.set(gcx, 20.0, gcz);

                    //  Тут будет раскраска торговых точек
//                    scene.traverse(obj => {
//                        if(obj instanceof THREE.Mesh) {
//                            console.log(obj.name);
//                            obj.material.color = new THREE.Color(0xff00ff);
//                        }
//                    });

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
}

export { View3D };