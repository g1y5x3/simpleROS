@0xb88514ec5705dc24;

struct Vector3 {
  x @0 :Float64;
  y @1 :Float64;
  z @2 :Float64;
}

struct Twist {
  linear @0 :Vector3;
  angular @1 :Vector3;
}