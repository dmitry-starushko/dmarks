{% load static %}
<script type="importmap"> {
    "imports": {
        "ts_chat": "{% static 'js/ts-chat.module.js' %}"
        ,"three": "{% static 'js/three/three.module.js' %}"
        ,"gltf_loader": "{% static 'js/three/loader/GLTFLoader.js' %}"
        ,"orbit_controls": "{% static 'js/three/controls/OrbitControls.js' %}"
        ,"map_controls": "{% static 'js/three/controls/MapControls.js' %}"
        ,"view3d": "{% static 'js/view3d.module.js' %}"
    }
}</script>