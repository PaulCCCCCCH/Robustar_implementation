# Robustar Frontend

Composed of two packages: `robustar` and `robustar-image-editor`. Packages are managed with `Lerna`.

`robustar-image-editor` is adopted from `tui.image-editor`

## Environment Setup for Developers

First, make sure you are in `front-end` folder, and have `npm` installed. Then, execute the following:

```
npm install -g webpack webpack-cli lerna prettier @vue/cli
```

Remember to run the above with `sudo` if you are in a linux/mac environment.

In `/front-end` folder, run

```
npm install
```

Finally, run the following command, which will automatically install dependencies for `robustar` and `robustar-image-editor`, and resolve the dependency between the two

```
lerna bootstrap
```

You are now all set with the environment.

## Important!

Before you push to remote repo, make sure you go back to `front-end` and run

```
prettier --write .
```

to fix any styling issues.

## Run locally

To run `robustar`, first build the `robustar-image-editor` with

```
lerna run build:editor --stream
```

Then, run `robustar` with

```
lerna run serve:main --stream
```

Note that whenever you make changes to `robustar-image-editor`, you will have to **build editor again** with `lerna run build:editor`, so that changes take effect on `robustar`. Alternatively, you could run editor alone to view real-time changes:

```
lerna run serve:editor --stream
```

## Notes

- Fabric Canvas object [doc](http://fabricjs.com/docs/fabric.Canvas.html#toCanvasElement). Use this to draw.
