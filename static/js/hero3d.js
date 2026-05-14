/**
 * Scalora – Hero 3D Background
 * Three.js particle field with connecting lines
 */

(function () {
  const canvas = document.getElementById('heroCanvas');
  if (!canvas || typeof THREE === 'undefined') return;

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setClearColor(0x000000, 0);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
  camera.position.z = 60;

  /* ── Particles ── */
  const PARTICLE_COUNT = 120;
  const positions = new Float32Array(PARTICLE_COUNT * 3);
  const velocities = [];
  const colors = new Float32Array(PARTICLE_COUNT * 3);

  const colorPalette = [
    new THREE.Color(0x1B3673),
    new THREE.Color(0x4A5D8A),
    new THREE.Color(0xc9b37e),
    new THREE.Color(0x8C92AC),
  ];

  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const spread = 80;
    positions[i * 3]     = (Math.random() - 0.5) * spread;
    positions[i * 3 + 1] = (Math.random() - 0.5) * spread * 0.6;
    positions[i * 3 + 2] = (Math.random() - 0.5) * 40;

    velocities.push(
      (Math.random() - 0.5) * 0.025,
      (Math.random() - 0.5) * 0.015,
      (Math.random() - 0.5) * 0.01
    );

    const col = colorPalette[Math.floor(Math.random() * colorPalette.length)];
    colors[i * 3]     = col.r;
    colors[i * 3 + 1] = col.g;
    colors[i * 3 + 2] = col.b;
  }

  const particleGeo = new THREE.BufferGeometry();
  particleGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  particleGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));

  const particleMat = new THREE.PointsMaterial({
    size: 1.2,
    vertexColors: true,
    transparent: true,
    opacity: 0.65,
    sizeAttenuation: true,
  });

  const particles = new THREE.Points(particleGeo, particleMat);
  scene.add(particles);

  /* ── Connection lines ── */
  const lineMat = new THREE.LineBasicMaterial({
    color: 0x4A5D8A,
    transparent: true,
    opacity: 0.12,
  });

  const linesGroup = new THREE.Group();
  scene.add(linesGroup);

  function updateLines() {
    // Clear old lines
    while (linesGroup.children.length) linesGroup.remove(linesGroup.children[0]);

    const pos = particleGeo.attributes.position.array;
    const maxDist = 18;
    const maxLines = 80;
    let lineCount = 0;

    for (let i = 0; i < PARTICLE_COUNT && lineCount < maxLines; i++) {
      for (let j = i + 1; j < PARTICLE_COUNT && lineCount < maxLines; j++) {
        const dx = pos[i*3]   - pos[j*3];
        const dy = pos[i*3+1] - pos[j*3+1];
        const dz = pos[i*3+2] - pos[j*3+2];
        const dist = Math.sqrt(dx*dx + dy*dy + dz*dz);

        if (dist < maxDist) {
          const geo = new THREE.BufferGeometry().setFromPoints([
            new THREE.Vector3(pos[i*3], pos[i*3+1], pos[i*3+2]),
            new THREE.Vector3(pos[j*3], pos[j*3+1], pos[j*3+2]),
          ]);
          const opacity = (1 - dist / maxDist) * 0.18;
          const mat = new THREE.LineBasicMaterial({ color: 0x4A5D8A, transparent: true, opacity });
          linesGroup.add(new THREE.Line(geo, mat));
          lineCount++;
        }
      }
    }
  }

  /* ── Floating geometric shapes ── */
  const shapes = [];
  const shapeGeos = [
    new THREE.OctahedronGeometry(1.5, 0),
    new THREE.TetrahedronGeometry(1.8, 0),
    new THREE.IcosahedronGeometry(1.2, 0),
  ];
  const shapeMat = new THREE.MeshBasicMaterial({
    color: 0xc9b37e,
    wireframe: true,
    transparent: true,
    opacity: 0.12,
  });

  for (let i = 0; i < 5; i++) {
    const mesh = new THREE.Mesh(
      shapeGeos[i % shapeGeos.length],
      shapeMat.clone()
    );
    mesh.position.set(
      (Math.random() - 0.5) * 70,
      (Math.random() - 0.5) * 40,
      (Math.random() - 0.5) * 20 - 10
    );
    mesh.userData.rotSpeed = {
      x: (Math.random() - 0.5) * 0.008,
      y: (Math.random() - 0.5) * 0.012,
    };
    mesh.userData.floatOffset = Math.random() * Math.PI * 2;
    scene.add(mesh);
    shapes.push(mesh);
  }

  /* ── Mouse parallax ── */
  let mouseX = 0, mouseY = 0;
  document.addEventListener('mousemove', (e) => {
    mouseX = (e.clientX / window.innerWidth - 0.5) * 2;
    mouseY = (e.clientY / window.innerHeight - 0.5) * 2;
  });

  /* ── Resize ── */
  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });

  /* ── Animation loop ── */
  let frame = 0;
  function animate() {
    requestAnimationFrame(animate);
    frame++;

    const pos = particleGeo.attributes.position.array;

    // Move particles
    for (let i = 0; i < PARTICLE_COUNT; i++) {
      pos[i*3]     += velocities[i*3];
      pos[i*3 + 1] += velocities[i*3 + 1];
      pos[i*3 + 2] += velocities[i*3 + 2];

      // Wrap around
      if (pos[i*3]     >  40) pos[i*3]     = -40;
      if (pos[i*3]     < -40) pos[i*3]     =  40;
      if (pos[i*3 + 1] >  24) pos[i*3 + 1] = -24;
      if (pos[i*3 + 1] < -24) pos[i*3 + 1] =  24;
      if (pos[i*3 + 2] >  20) pos[i*3 + 2] = -20;
      if (pos[i*3 + 2] < -20) pos[i*3 + 2] =  20;
    }

    particleGeo.attributes.position.needsUpdate = true;

    // Update lines every 4 frames for performance
    if (frame % 4 === 0) updateLines();

    // Rotate shapes
    const t = frame * 0.016;
    shapes.forEach(s => {
      s.rotation.x += s.userData.rotSpeed.x;
      s.rotation.y += s.userData.rotSpeed.y;
      s.position.y += Math.sin(t + s.userData.floatOffset) * 0.008;
    });

    // Subtle camera parallax
    camera.position.x += (mouseX * 4 - camera.position.x) * 0.04;
    camera.position.y += (-mouseY * 2 - camera.position.y) * 0.04;
    camera.lookAt(scene.position);

    renderer.render(scene, camera);
  }

  // Initial lines
  updateLines();
  animate();
})();
