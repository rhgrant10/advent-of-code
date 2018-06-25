Hex Ed
======

Use a 3d grid, like Q*bert :)

```
  y
   \ 
    \ _ _ _ x
   /
  /
z
```

```
   y
    \  n   /
  nw +----+ ne
    /      \
  -+        +- x
    \      /
  sw +----+ se
    /  s   \
   z
```

```
   y
    \ 0+-  /
-+0  +---+  +0-
    /     \
---+       +--- x
    \     /
-0+  +---+  +-0
    / 0-+  \
   z
```

The resulting distance formula is simple:

```
d = max(x2 - x1, y2 - y1, z2 - z1)
```
