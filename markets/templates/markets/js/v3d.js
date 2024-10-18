const v3d = document.getElementById("{{div_id}}");
const width = v3d.clientWidth, height = v3d.clientHeight;
const camera = new THREE.PerspectiveCamera( 70, width / height, 0.01, 10 );
camera.position.z = 1;
const scene = new THREE.Scene();
const geometry = new THREE.BoxGeometry(0.2, 0.2, 0.2);
const material = new THREE.MeshNormalMaterial();
const mesh = new THREE.Mesh(geometry, material);
scene.add(mesh);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(width, height);
renderer.setAnimationLoop(animate);
v3d.appendChild(renderer.domElement);

function animate(time) {
	mesh.rotation.x = time / 2000;
	mesh.rotation.y = time / 1000;
	renderer.render(scene, camera);
}