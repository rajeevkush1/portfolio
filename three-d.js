/* =============================================================================
   three-d.js — Portfolio 3D Animations via Three.js
   - Hero:    Rotating wireframe icosahedron + floating particle field
   - Skills:  Orbiting torus rings
   - Connect: Animated neural node graph (nodes + glowing edges)
   All canvases: pointer-events: none, respects prefers-reduced-motion
============================================================================= */

(function () {
    'use strict';

    if (typeof THREE === 'undefined') return;

    const REDUCED = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function fitCanvas(renderer, camera, canvas) {
        const w = canvas.parentElement.offsetWidth;
        const h = canvas.parentElement.offsetHeight;
        renderer.setSize(w, h, false);
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
    }

    /* ── 1. HERO: Wireframe icosahedron + particle cloud ── */
    (function initHero() {
        const canvas = document.getElementById('heroCanvas');
        if (!canvas) return;

        const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(60, 1, 0.1, 100);
        camera.position.set(0, 0, 5);
        fitCanvas(renderer, camera, canvas);

        const icoGeo = new THREE.IcosahedronGeometry(1.5, 1);
        const icoMat = new THREE.MeshBasicMaterial({ color: 0x6366f1, wireframe: true, transparent: true, opacity: 0.55 });
        const ico = new THREE.Mesh(icoGeo, icoMat);
        ico.position.set(2.5, 0, 0);
        scene.add(ico);

        const coreGeo = new THREE.IcosahedronGeometry(0.9, 1);
        const coreMat = new THREE.MeshBasicMaterial({ color: 0xa855f7, transparent: true, opacity: 0.12 });
        ico.add(new THREE.Mesh(coreGeo, coreMat));

        const N = 180;
        const pos = new Float32Array(N * 3);
        for (let i = 0; i < N; i++) {
            pos[i*3]   = (Math.random()-0.5)*12;
            pos[i*3+1] = (Math.random()-0.5)*8;
            pos[i*3+2] = (Math.random()-0.5)*6;
        }
        const partGeo = new THREE.BufferGeometry();
        partGeo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
        const partMat = new THREE.PointsMaterial({ color: 0x6366f1, size: 0.045, transparent: true, opacity: 0.65 });
        scene.add(new THREE.Points(partGeo, partMat));

        let mx = 0, my = 0;
        document.addEventListener('mousemove', e => {
            mx = (e.clientX / window.innerWidth - 0.5) * 2;
            my = (e.clientY / window.innerHeight - 0.5) * 2;
        });
        window.addEventListener('resize', () => fitCanvas(renderer, camera, canvas));

        const clock = new THREE.Clock();
        (function animate() {
            requestAnimationFrame(animate);
            const t = clock.getElapsedTime();
            if (!REDUCED) {
                ico.rotation.x = t*0.18 + my*0.25;
                ico.rotation.y = t*0.28 + mx*0.25;
                camera.position.x += (mx*0.3 - camera.position.x)*0.05;
                camera.position.y += (-my*0.2 - camera.position.y)*0.05;
                camera.lookAt(scene.position);
            }
            renderer.render(scene, camera);
        })();
    })();

    /* ── 2. SKILLS: Orbiting torus rings ── */
    (function initSkills() {
        const canvas = document.getElementById('skillsCanvas');
        if (!canvas) return;

        const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(55, 1, 0.1, 100);
        camera.position.set(0, 0, 7);
        fitCanvas(renderer, camera, canvas);

        const addTorus = (r, tube, color, opacity, rx, ry, rz) => {
            const m = new THREE.Mesh(
                new THREE.TorusGeometry(r, tube, 12, 80),
                new THREE.MeshBasicMaterial({ color, transparent: true, opacity, wireframe: false })
            );
            m.rotation.set(rx||0, ry||0, rz||0);
            scene.add(m);
            return m;
        };
        const t1 = addTorus(3.0, 0.04, 0x6366f1, 0.35, Math.PI/3);
        const t2 = addTorus(2.0, 0.035, 0xec4899, 0.30, Math.PI/5, 0, Math.PI/4);
        const t3 = addTorus(1.2, 0.03, 0xa855f7, 0.28, 0, Math.PI/6);

        const dot = new THREE.Mesh(
            new THREE.SphereGeometry(0.09, 8, 8),
            new THREE.MeshBasicMaterial({ color: 0x6366f1 })
        );
        scene.add(dot);

        window.addEventListener('resize', () => fitCanvas(renderer, camera, canvas));
        const clock = new THREE.Clock();
        (function animate() {
            requestAnimationFrame(animate);
            const t = clock.getElapsedTime();
            if (!REDUCED) {
                t1.rotation.z = t*0.15;
                t2.rotation.z = -t*0.22;
                t2.rotation.x = Math.PI/5 + t*0.08;
                t3.rotation.x = t*0.3;
                t3.rotation.y = t*0.18;
                dot.position.set(
                    3*Math.cos(t*0.4)*Math.cos(Math.PI/3),
                    3*Math.sin(t*0.4),
                    3*Math.cos(t*0.4)*Math.sin(Math.PI/3)
                );
            }
            renderer.render(scene, camera);
        })();
    })();

    /* ── 3. CONNECT: Neural node graph ── */
    (function initConnect() {
        const canvas = document.getElementById('connectCanvas');
        if (!canvas) return;

        const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(50, 1, 0.1, 100);
        camera.position.set(0, 0, 8);
        fitCanvas(renderer, camera, canvas);

        const N = 28;
        const colors = [0x6366f1, 0xec4899, 0xa855f7, 0x06b6d4];
        const meshes = [], nodePos = [], vels = [];
        const nodeGeo = new THREE.SphereGeometry(0.08, 8, 8);
        const group = new THREE.Group();

        for (let i = 0; i < N; i++) {
            const mat = new THREE.MeshBasicMaterial({ color: colors[i%4], transparent: true, opacity: 0.85 });
            const m = new THREE.Mesh(nodeGeo, mat);
            const p = new THREE.Vector3((Math.random()-0.5)*10, (Math.random()-0.5)*6, (Math.random()-0.5)*4);
            m.position.copy(p);
            nodePos.push(p.clone());
            meshes.push(m);
            group.add(m);
            vels.push(new THREE.Vector3((Math.random()-0.5)*0.003, (Math.random()-0.5)*0.003, (Math.random()-0.5)*0.002));
        }

        const edgeMat = new THREE.LineBasicMaterial({ color: 0x6366f1, transparent: true, opacity: 0.2 });
        for (let i = 0; i < N; i++) {
            for (let j = i+1; j < N; j++) {
                if (nodePos[i].distanceTo(nodePos[j]) < 3.5) {
                    const geo = new THREE.BufferGeometry().setFromPoints([nodePos[i], nodePos[j]]);
                    group.add(new THREE.Line(geo, edgeMat));
                }
            }
        }

        scene.add(group);
        window.addEventListener('resize', () => fitCanvas(renderer, camera, canvas));

        const clock = new THREE.Clock();
        (function animate() {
            requestAnimationFrame(animate);
            const t = clock.getElapsedTime();
            if (!REDUCED) {
                meshes.forEach((m, i) => {
                    m.position.add(vels[i]);
                    ['x','y','z'].forEach(ax => {
                        const lim = ax==='z'?2:ax==='y'?3:5;
                        if (Math.abs(m.position[ax]) > lim) vels[i][ax] *= -1;
                    });
                });
                group.rotation.y = t*0.06;
                group.rotation.x = Math.sin(t*0.04)*0.15;
            }
            renderer.render(scene, camera);
        })();
    })();

})();
