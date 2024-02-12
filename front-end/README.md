# Robustar Frontend

Composed of two packages: `robustar` and `robustar-image-editor`. Packages are managed with [Lerna](https://lerna.js.org/docs/getting-started) and [npm workspaces](https://docs.npmjs.com/cli/v7/using-npm/workspaces).

`robustar-image-editor` is adopted from [tui.image-editor](https://ui.toast.com/tui-image-editor)

## Environment Setup for Developers

First, make sure you are in `front-end` folder, and have Node.js (>= 15) and npm installed.

In `/front-end` folder, run

```
npm install
```

You are now all set with the environment.

## Run locally

To run `robustar`, first build the `robustar-image-editor` with

```
npm run build:editor
```

Then, run `robustar` with

```
npm run serve:main
```

Note that whenever you make changes to `robustar-image-editor`, you will have to **build editor again** with `npm run build:editor`, so that changes take effect on `robustar`. Alternatively, you can run editor alone to view real-time changes:

```
npm run serve:editor
```

To use Cypress for E2E testing, you can run the following command:

```
npm run cypress:open
```

## Notes

- Fabric Canvas object [doc](http://fabricjs.com/docs/fabric.Canvas.html#toCanvasElement). Use this to draw.
