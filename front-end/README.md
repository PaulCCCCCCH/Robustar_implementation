# Robustar Frontend

Composed of two packages: `robustar` and `robustar-image-editor`. Packages are managed with `Lerna`.

`robustar-image-editor` is adopted from `tui.image-editor`

## Environment Setup for Developers

First, make sure you are in `front-end` folder, and have `npm` installed.

In `/front-end` folder, run

```
npm install
```

You are now all set with the environment.

## Run locally

To run `robustar`, first build the `robustar-image-editor` with

```
npx lerna run build:editor --stream
```

Then, run `robustar` with

```
npx lerna run serve:main --stream
```

Note that whenever you make changes to `robustar-image-editor`, you will have to **build editor again** with `npx lerna run build:editor`, so that changes take effect on `robustar`. Alternatively, you could run editor alone to view real-time changes:

```
npx lerna run serve:editor --stream
```

## Notes

- Fabric Canvas object [doc](http://fabricjs.com/docs/fabric.Canvas.html#toCanvasElement). Use this to draw.
