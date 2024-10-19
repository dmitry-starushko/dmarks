const v3d = document.getElementById("{{div_id}}");
const width = v3d.clientWidth, height = v3d.clientHeight;
const camera = new THREE.PerspectiveCamera(60, width / height, 0.01, 10000);
camera.position.z = 1;
camera.position.x = 7;
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x11aabb)

const geometry = new THREE.BoxGeometry(0.2, 0.2, 0.2);
const material = new THREE.MeshNormalMaterial();
const mesh = new THREE.Mesh(geometry, material);
scene.add(mesh);

const loader = new GLTFLoader();
loader.load(
    "{% url 'api:schemes_take_gltf' scheme_pk=sch_pk %}",
    function(gltf) {
        scene.add(gltf.scene);

//        scene.traverse(obj => {
//            if(obj instanceof THREE.Mesh) {
//                obj.material.color = new THREE.Color(0xff00ff);
//            }
//        });

        const ground = gltf.scene.getObjectByName("ground");

        if(ground) {
            const bbx_min = ground.geometry.boundingBox.min;
            const bbx_max = ground.geometry.boundingBox.max;
            const gcx = 0.5 * (bbx_min.x + bbx_max.x);
            const gcz = 0.5 * (bbx_min.z + bbx_max.z);
            const ab_light = new THREE.AmbientLight(0xffffffff);
            scene.add(ab_light);
            const dir_light = new THREE.DirectionalLight( 0xffffff, 10 );
            let dir_light_t = new THREE.Object3D();
            dir_light_t.position.set(dir_light.position.x+1,0,dir_light.position.z+1);
            scene.add(dir_light_t);
            dir_light.target = dir_light_t;
            scene.add(dir_light);
            camera.position.set(gcx, 7.0, gcz);
        }
    },
    function(progress) { console.log((progress.loaded / progress.total) * 100 + "% loaded"); },
    function(error) { console.error(error); });

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.shadowMap.enabled = true;
renderer.setSize(width, height);
renderer.setAnimationLoop(animate);
v3d.appendChild(renderer.domElement);

function animate(time) {
	{# mesh.rotation.x = time / 2000; 	mesh.rotation.y = time / 1000; #}
//	camera.position.x = 2138+time / 500;
//	camera.position.y = 7;
//	camera.position.z = 1261+time / 100;
    camera.rotation.y = time / 4000;
	renderer.render(scene, camera);
}