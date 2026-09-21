(function() {
  const canvas = document.getElementById('radarCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d', { alpha: true, desynchronized: true });
  const w = canvas.width, h = canvas.height;
  const cx = w/2, cy = h/2;
  const radius = Math.min(w, h) * 0.38;

  const shieldImage = new Image();
  shieldImage.crossOrigin = 'anonymous';
  shieldImage.src = '/images/schit.jpg';
  let shieldLoaded = false, animStarted = false, angle = 0, animId = null;

  shieldImage.onload = () => { shieldLoaded = true; if (!animStarted) { animStarted = true; drawRadar(); } };
  shieldImage.onerror = () => { shieldLoaded = false; if (!animStarted) { animStarted = true; drawRadar(); } };

  let glowGrad, lineGrad, arrowGrad;
  function getGradients() {
    if (!glowGrad) {
      glowGrad = ctx.createRadialGradient(cx, cy, radius*0.2, cx, cy, radius*1.4);
      glowGrad.addColorStop(0, 'rgba(240, 178, 74, 0.25)');
      glowGrad.addColorStop(0.5, 'rgba(240, 178, 74, 0.08)');
      glowGrad.addColorStop(1, 'rgba(240, 178, 74, 0)');
    }
    if (!lineGrad) {
      lineGrad = ctx.createLinearGradient(0, 0, radius, 0);
      lineGrad.addColorStop(0, 'rgba(240, 178, 74, 1)');
      lineGrad.addColorStop(0.4, 'rgba(255, 211, 126, 0.9)');
      lineGrad.addColorStop(0.7, 'rgba(240, 178, 74, 0.5)');
      lineGrad.addColorStop(1, 'rgba(240, 178, 74, 0)');
    }
    if (!arrowGrad) {
      arrowGrad = ctx.createRadialGradient(0, 0, 2, 0, 0, 20);
      arrowGrad.addColorStop(0, 'rgba(255, 211, 126, 1)');
      arrowGrad.addColorStop(1, 'rgba(240, 178, 74, 0)');
    }
    return { glowGrad, lineGrad, arrowGrad };
  }

  const MAX_TARGETS = 15;
  const targets = [];
  function createTarget(angle, dist, speed) {
    return {
      angle: angle || Math.random() * 2 * Math.PI,
      dist: dist || radius * (0.60 + 0.35 * Math.random()),
      speed: speed || 0.002 + 0.003 * Math.random(),
      hit: false, detectTime: 0, fading: false, fadeTimer: 0, opacity: 1
    };
  }
  for (let i = 0; i < 3; i++) targets.push(createTarget());

  let particles = [];
  class Particle {
    constructor(x, y, color) {
      this.x = x; this.y = y;
      this.vx = (Math.random() - 0.5) * 8;
      this.vy = (Math.random() - 0.5) * 8;
      this.life = 1;
      this.decay = 0.015 + Math.random() * 0.025;
      this.size = 2 + Math.random() * 4;
      this.color = color || '#FFD37E';
    }
    update() {
      this.x += this.vx; this.y += this.vy;
      this.vx *= 0.98; this.vy *= 0.98;
      this.life -= this.decay;
      return this.life > 0;
    }
    draw(ctx) {
      ctx.save();
      ctx.globalAlpha = this.life;
      ctx.fillStyle = this.color;
      ctx.shadowBlur = 15;
      ctx.shadowColor = this.color;
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size * this.life, 0, 2 * Math.PI);
      ctx.fill();
      ctx.restore();
    }
  }
  function spawnSparks(x, y, count, color) {
    for (let i = 0; i < count; i++) particles.push(new Particle(x, y, color));
  }

  let shockwaves = [];
  class Shockwave {
    constructor(x, y, color) {
      this.x = x; this.y = y;
      this.radius = 0; this.maxRadius = 100; this.speed = 3; this.opacity = 1;
      this.color = color || '#FFD37E';
    }
    update() {
      this.radius += this.speed;
      this.opacity = 1 - (this.radius / this.maxRadius);
      return this.opacity > 0;
    }
    draw(ctx) {
      ctx.save();
      ctx.globalAlpha = this.opacity * 0.6;
      ctx.strokeStyle = this.color;
      ctx.lineWidth = 3;
      ctx.shadowBlur = 30;
      ctx.shadowColor = this.color;
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius, 0, 2 * Math.PI);
      ctx.stroke();
      ctx.restore();
    }
  }

  function drawRadar() {
    ctx.clearRect(0, 0, w, h);

    if (shieldLoaded) {
      ctx.save();
      ctx.drawImage(shieldImage, 0, 0, w, h);
      ctx.restore();
    } else {
      ctx.fillStyle = '#0D1420';
      ctx.fillRect(0, 0, w, h);
      ctx.fillStyle = '#FFD37E';
      ctx.font = 'bold 56px "Cormorant", Georgia, serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('РУСКОРПОРАЦИЯ', cx, cy-20);
      ctx.font = '22px "Manrope", sans-serif';
      ctx.fillStyle = '#8FA1B5';
      ctx.fillText('ОХРАНА И КОНСАЛТИНГ', cx, cy+50);
    }

    const grads = getGradients();
    ctx.save();

    ctx.fillStyle = grads.glowGrad;
    ctx.beginPath();
    ctx.arc(cx, cy, radius * 1.3, 0, 2 * Math.PI);
    ctx.fill();

    ctx.translate(cx, cy);
    ctx.strokeStyle = 'rgba(240, 178, 74, 0.2)';
    ctx.lineWidth = 1.5;
    for (let r = radius * 0.2; r <= radius; r += radius * 0.2) {
      ctx.beginPath();
      ctx.arc(0, 0, r, 0, 2 * Math.PI);
      ctx.stroke();
    }
    ctx.strokeStyle = 'rgba(240, 178, 74, 0.12)';
    for (let i = 0; i < 8; i++) {
      const a = (i * Math.PI / 4) + angle * 0.01;
      ctx.beginPath();
      ctx.moveTo(0, 0);
      ctx.lineTo(radius * Math.cos(a), radius * Math.sin(a));
      ctx.stroke();
    }

    ctx.rotate(angle);
    ctx.shadowColor = 'rgba(240, 178, 74, 0.9)';
    ctx.shadowBlur = 40;
    ctx.strokeStyle = grads.lineGrad;
    ctx.lineWidth = 5;
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(radius * 1.02, 0);
    ctx.stroke();

    ctx.shadowBlur = 30;
    ctx.fillStyle = grads.arrowGrad;
    ctx.beginPath();
    ctx.arc(0, 0, 14, 0, 2 * Math.PI);
    ctx.fill();
    ctx.restore();

    // Цели
    for (let i = targets.length - 1; i >= 0; i--) {
      const t = targets[i];
      if (!t.hit && !t.fading) {
        t.dist -= t.speed * radius * 0.6;
        if (t.dist < radius * 0.25) { // не долетают до центра
          targets.splice(i, 1);
          continue;
        }
      }
      if (t.fading) {
        t.fadeTimer -= 0.016;
        t.opacity = Math.max(0, t.fadeTimer / 2);
        if (t.fadeTimer <= 0) {
          if (targets.length < MAX_TARGETS) {
            const toAdd = Math.min(2, MAX_TARGETS - targets.length);
            for (let j = 0; j < toAdd; j++) targets.push(createTarget());
          }
          targets.splice(i, 1);
          continue;
        }
      }
      const x = cx + t.dist * Math.cos(t.angle);
      const y = cy + t.dist * Math.sin(t.angle);

      if (!t.hit && !t.fading) {
        let diff = t.angle - angle;
        diff = ((diff % (2 * Math.PI)) + 3 * Math.PI) % (2 * Math.PI) - Math.PI;
        if (Math.abs(diff) < 0.08 && t.dist > radius * 0.12) {
          t.hit = true;
          t.detectTime = 1;
          spawnSparks(x, y, 25, '#FFD37E');
          shockwaves.push(new Shockwave(x, y, '#FFD37E'));
          spawnSparks(x, y, 10, '#FFFFFF');
        }
      }
      if (t.detectTime > 0 && !t.fading) {
        t.detectTime -= 0.03;
        if (t.detectTime <= 0 && t.hit) {
          t.fading = true;
          t.fadeTimer = 2;
        }
      }

      const alpha = t.fading ? t.opacity : (0.6 + 0.4 * (t.dist / radius));
      const size = 10 * (0.6 + 0.4 * (t.dist / radius));
      const pulse = t.detectTime > 0 && !t.fading ? size * (1 + t.detectTime * 0.8) : size;
      const color = t.hit ? '#FFD37E' : '#FF4444';
      const shadow = t.hit ? 'rgba(255, 211, 126, 0.9)' : 'rgba(255, 68, 68, 0.9)';

      ctx.save();
      ctx.shadowColor = shadow;
      ctx.shadowBlur = t.hit ? 50 : 25;
      ctx.fillStyle = color;
      ctx.globalAlpha = alpha;
      ctx.beginPath();
      ctx.arc(x, y, pulse, 0, 2 * Math.PI);
      ctx.fill();

      ctx.shadowBlur = 0;
      ctx.fillStyle = 'rgba(255,255,255,0.4)';
      ctx.beginPath();
      ctx.arc(x - pulse*0.2, y - pulse*0.2, pulse*0.25, 0, 2 * Math.PI);
      ctx.fill();
      ctx.restore();
    }

    shockwaves = shockwaves.filter(sw => {
      const active = sw.update();
      if (active) sw.draw(ctx);
      return active;
    });

    particles = particles.filter(p => {
      const active = p.update();
      if (active) p.draw(ctx);
      return active;
    });

    ctx.save();
    ctx.shadowColor = 'rgba(240, 178, 74, 0.3)';
    ctx.shadowBlur = 40;
    ctx.strokeStyle = 'rgba(240, 178, 74, 0.25)';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(cx, cy, radius, 0, 2 * Math.PI);
    ctx.stroke();
    ctx.restore();

    ctx.save();
    ctx.fillStyle = 'rgba(240, 178, 74, 0.7)';
    ctx.font = 'bold 15px "Manrope", sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'bottom';
    ctx.shadowBlur = 20;
    ctx.shadowColor = 'rgba(240, 178, 74, 0.3)';
    ctx.fillText('• СКАНИРОВАНИЕ •', cx, cy + radius + 50);
    ctx.restore();

    angle += 0.02;
    animId = requestAnimationFrame(drawRadar);
  }

  if (shieldImage.complete && shieldImage.naturalWidth !== 0) {
    shieldLoaded = true;
    animStarted = true;
    drawRadar();
  } else {
    setTimeout(() => {
      if (!animStarted) {
        animStarted = true;
        drawRadar();
      }
    }, 3000);
  }

  window.addEventListener('beforeunload', () => {
    if (animId) cancelAnimationFrame(animId);
  });
})();
