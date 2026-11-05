/*
 * Shared Larpidie atlas -> 3D transform.
 * Atlas coordinates are local kilometres from the north-west frame corner:
 * x grows east and y grows south (SVG/DEM row order). WebGL uses the
 * right-handed basis +X east, +Y elevation, +Z south. All horizontal values
 * are kilometres and all elevations are metres converted to kilometres.
 */
(() => {
  const CENTER_X_KM = 14.65;
  const CENTER_Y_KM = 9.5;
  const toWorld = (xKm, yKm) => [xKm - CENTER_X_KM, yKm - CENTER_Y_KM];
  const toAtlas = (x, z) => [x + CENTER_X_KM, z + CENTER_Y_KM];
  const gridToWorld = (col, row, grid) => toWorld(
    grid.origin_xy_km[0] + col * grid.sample_m / 1000,
    grid.origin_xy_km[1] + row * grid.sample_m / 1000,
  );

  window.LARPIDIA_ATLAS_WORLD = Object.freeze({
    axes: "+X east, +Y up, +Z south; north is -Z",
    horizontalUnit: "km",
    verticalUnit: "km",
    seaLevelM: 0,
    centerAtlasKm: Object.freeze([CENTER_X_KM, CENTER_Y_KM]),
    toWorld,
    toAtlas,
    gridToWorld,
  });
})();
