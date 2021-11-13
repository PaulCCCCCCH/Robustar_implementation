# Robustar Frontend

Composed of two packages: `robustar` and `robustar-image-editor`. Packages are managed with `Lerna`. 

`robustar-image-editor` is adopted from `tui.image-editor`



## Environment Setup for Developers

First, make sure you are in `front-end` folder, and have `npm` installed. Then, execute the following:

```
npm install -g webpack webpack-cli lerna
```

This command will automatically install dependencies for `robustar` and `robustar-image-editor`, and resolve the dependency between the two

```
lerna bootstrap
```

You are now all set with the environment.



## Run locally

To run `robustar`, first build the `robustar-image-editor` with

```
lerna run build:editor
```

Then, run `robustar` with

```
lerna run serve:main
```

Note that whenever you make changes to `robustar-image-editor`, you will have to **build editor again** with `lerna run build:editor`, so that changes take effect on `robustar`. Alternatively, you could run editor alone to view real-time changes:

```
lerna run serve:editor
```





 





