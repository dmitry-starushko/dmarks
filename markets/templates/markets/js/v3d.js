const v3d = document.getElementById("{{div_id}}");
const width = v3d.clientWidth, height = v3d.clientHeight;
const camera = new THREE.PerspectiveCamera(90, width / height, 0.01, 10000);
camera.position.z = 1;
camera.position.x = 1;
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xaaaaaa)
{% comment %}
const geometry = new THREE.BoxGeometry(0.2, 0.2, 0.2);
const material = new THREE.MeshNormalMaterial();
const mesh = new THREE.Mesh(geometry, material);
scene.add(mesh);
{% endcomment %}
const loader = new GLTFLoader();
loader.load(
    "{% url 'api:schemes_take_gltf' scheme_pk=1359 %}",
    function(gltf) { scene.add(gltf.scene); },
    function(progress) { console.log((progress.loaded / progress.total) * 100 + "% loaded"); },
    function(error) { console.error(error); });
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(width, height);
renderer.setAnimationLoop(animate);
v3d.appendChild(renderer.domElement);

function animate(time) {
	{# mesh.rotation.x = time / 2000; 	mesh.rotation.y = time / 1000; #}
	camera.position.x = 2138+time / 500;
	camera.position.y = 7;
	camera.position.z = 1261+time / 500;
	renderer.render(scene, camera);
}