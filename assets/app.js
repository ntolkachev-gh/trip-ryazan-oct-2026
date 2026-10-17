document.addEventListener('DOMContentLoaded',()=>{
const b=document.querySelector('.burger');b&&(b.onclick=()=>b.closest('nav').classList.toggle('open'));
document.querySelectorAll('.cl input').forEach((c,i)=>{const k='ryz-cl-'+i;c.checked=localStorage.getItem(k)==='1';c.onchange=()=>localStorage.setItem(k,c.checked?'1':'0')});
const io=new IntersectionObserver(e=>e.forEach(x=>{if(x.isIntersecting){x.target.classList.add('on');io.unobserve(x.target)}}),{threshold:.05});
document.querySelectorAll('.rv').forEach(el=>io.observe(el));
const D=window.TRIP;if(!D||!window.L)return;
const icon=d=>L.divIcon({className:'',html:`<div class="mk" style="background:${D.colors[d]}">${d}</div>`,iconSize:[30,30],iconAnchor:[15,15]});
const tiles=m=>L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',{attribution:'© OpenStreetMap © CARTO',subdomains:'abcd'}).addTo(m);
document.querySelectorAll('[data-map]').forEach(el=>{
 const only=el.dataset.map==='all'?null:+el.dataset.map;const m=L.map(el,{scrollWheelZoom:false});tiles(m);
 const layers={};D.points.filter(p=>!only||p.day===only).forEach(p=>{const mk=L.marker([p.lat,p.lon],{icon:icon(p.day)}).bindPopup(`<b>День ${p.day}</b><br>${p.name}`);(layers[p.day]=layers[p.day]||L.layerGroup().addTo(m)).addLayer(mk)});
 const all=Object.values(layers).flatMap(g=>g.getLayers());if(all.length>1)m.fitBounds(L.featureGroup(all).getBounds().pad(.25));else m.setView(all[0].getLatLng(),10);
 document.querySelectorAll('.flt button').forEach(bt=>bt.onclick=()=>{bt.classList.toggle('on');const g=layers[bt.dataset.d];g&&(bt.classList.contains('on')?g.addTo(m):m.removeLayer(g))});
});});
