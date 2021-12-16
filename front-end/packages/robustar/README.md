# Front End

Developed with `Vue2`

## Project Structure

### Key Folders

- `src/router`: Defines the mapping between url and component to be rendered. E.g. Entering `localhost:8080/train` will show you the `src/components/Train.vue` component.
- `src/view`: Defines different views. We define a `view` to be an aggregation of `components`. E.g. `Home.vue` is composed of `Header` (`src/components/Header.vue`), `SideBar` (`src/components/SideBar.vue`), and some other stuff (depending on the url).
- `src/components`: Defines reusable components. Components are further divided into sub-folders for clarity.
- `src/assets`: Stores different resource files, e.g. icons and images.
- `src/utils`: Contains reusable utility functions written in pure javascript, e.g. a function that converts image id to image path.
- `src/apis`: Each file here contains a group of api calls to the backend, e.g. calls to start/pause/stop/inspect training grouped in `src/apis/train.js`.

### Key Files

- `src/App.vue`: Defines the root `Vue` object to which all other `Vue` components will be attached.
- `src/main.css`: Global styles.
- `src/main.js`: Entry point of the entire website. It attaches the root `Vue` object to the root `DOM`.
- `src/configs.js`: Stores constants that are used across the app, e.g. `ImageList` shows `3` \* `6` images per page.

## Run

```
    npm install
    npm run serve
```

## TODO List

- Cannot view misclassified and correctly classified images separately
- Drawing Functionalities
- Viewing influence

## Bug List

### ImageList

- `Next Page` calls `currentPage++` without bounding.
