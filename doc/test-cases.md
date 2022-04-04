# Overview
Test cases in lists/tables for each section should be run in given orders.

# Requirements

Make sure [Google Chrome](https://www.google.com/chrome/) has been installed on your machine before running the frontend tests.

# Setup
Make sure what's under `/Robustar2` is the same as [this one](https://drive.google.com/file/d/1WGicmBCHMFgLU70qwBTV4ffZ-RhpGKD-/view?usp=sharing).

`/Robustar2/configs.json` Should look like this. 

```
{
    "weight_to_load": "resnet-18.pth",
    "model_arch": "resnet-18-32x32",
    "device": "cpu",
    "pre_trained": false,
    "batch_size": 16,
    "shuffle": true,
    "num_workers": 8,
    "image_size": 32,
    "image_padding": "none",
    "num_classes": 9
}
```

# Cleanup
Delete `Robustar2/dataset/paired` and `*.txt` in `Robustar2/dataset`.


# Frontend

## Annotation - Normal Flow
- Click on `GOTO CLASS` button after selecting `cat` goes to page 125. 
- Click on `NEXT PAGE` goes to page 126. `url` in image should be different.
- Click on `GOTO PAGE` after inputing page number 9999. Expect page number and `train` in session storage to both be 1124.
- Expect `NEXT PAGE` to be disabled.
- Click `PREV PAGE` returns to page 1123. Expect page number and `train` in session storage to both be 1124.
- Click on `Annotate` on the first image of page 1123, expect session storage to contain: split = "train", annotated = 0.
- Click on `Send Edit`, wait for loading. Expect `image_url` in sessionStorage to be different.
- Click on `Send Edit` again, wait for loading. Expect `image_url` in sessionStorage to be different.
- Click on `Send Edit` again, wait for loading. Expect `image_url` in sessionStorage to be different.
- Go to `Annotated` page, expect 3 images on first page.
- Click on `Annotate` on the first image. Click on `Send Edit` twice, and go back to `Annotated` page. Expect the same three images in the same order (compare their urls)
- Go to `Auto Annotate` page, set the number to be 5, and start auto annotation. Task center component should now have 1 task in it.
- Wait for 10 seconds, the task center should be empty.
- Go back to `Annotated` page. There should be 6 images in it.
- Go back to `Training Data` page. page number should still be 1123. The url of the first image should be the same as the url of first annotated image.

## Annotation - Editing Validation Set
- Go to `Validation Data` page, click `Annotate` on the first image. Click `Send Edit`. Expect failure (Annotated list should not change).
- Go to `Test Data` page, click `Annotate` on the first image. Click `Send Edit`. Expect failure (Annotated list should not change).



## Test - Normal Flow
- Go to `Test` page, click on `START TESTING ON VALIDATION SET`. 
- Expect task center to have 1 task.
- Wait for 30 seconds for it to finish. Go to `Validation Data` page. Expect 8 images.
- Select `Incorrectly Classified` in the top dropdown. Expect 8 images.
- Go to `Test` , click on `START TESTING ON TEST SET`. 
- Expect task center to have 1 task.
- Wait for 30 seconds for it to finish. Go to `Test Data` page. Expect 8 images.
- Select `Incorrectly Classified` in the top dropdown. Expect 8 images.

## Training - Zero Epoch
- Go to `Train` page. Set epoch to 0. Expect nothing in task center.

## Training - Normal Flow
- Go to `Train` page, click on `START TRAINING` twice. There should be two processes in task center. 
- Click on `STOP TRAINING`. Two tasks should be exited, 0 process in task center.
- Click on `START TRAINING` twice. Click the red remove button at the front the one task in task center, expect that task to exit. Only 1 process remains in task center.


# Backend

## Get server configuration `GET /config`
Start server with the any `configs.json`. The API should return exactly the same thing.

## Edit image `POST /edit/<split>/<image_id>`  and `GET /propose/<split>/<image_id>`
Make sure to run the following in the given order.
| param | output |
| -- | -- |
| `split` is not `'train'` or `'annotated'`  | response.fail |
| large `image_id` (out of bound) | response.fail |
| `split = 'train', image_id = 9 ` | `bird/106.JPEG` annotated, first row of `/Robustar2/annotated.txt` is 9 |
| `split = 'train', image_id = 13 ` | `bird/11.JPEG` annotated, second row of `/Robustar2/annotated.txt` is 13 |
| `split = 'train', image_id = 9 ` | `bird/106.JPEG` annotated, content of `/Robustar2/annotated.txt` is `9\n13` |
| `split = 'annotated', image_id = 0 ` | `bird/106.JPEG` annotated, content of `/Robustar2/annotated.txt` is `9\n13` |

## Auto-annotate `POST /auto-annotate/<split>`
Run `Cleanup` step first (see the section above).
| param | output |
| -- | -- |
| `split` is not `'train'` | response.fail |
| `data.num_to_gen < 0` | response.fail |
| `data.num_to_gen = 0` | response.ok |
| `data.num_to_gen > length of dataset` | response.ok, trying to annotate entire dataset (no need to actually run) |
| `data.num_to_gen = 4` | response.ok, `bird/0.JPEG`, `bird/1.JPEG`, `bird/10.JPEG` and `bird/100.JPEG` annotated |

## Get image `GET /image/<split>/<image_id>`
| param | output |
| -- | -- |
| An invalid split, e.g., `split = 'non-exist'` | response.fail |
| `image_id` out of bound | response.fail |
| `image_id = 2, split = 'train'` | redirect to `dataset/Robustar2/dataset/bird/10.JPEG` |

## Get annotated image `GET /image/get-annotated/<image_id>`
| param | output |
| -- | -- |
| An invalid split, e.g., `split = 'non-exist'` | response.fail |
| `image_id` out of bound | response.fail |
| `image_id = 2` | return 2 |

## Get class lengths `GET /image/class/<split>`
| param | output |
| -- | -- |
| An invalid split, e.g., `split = 'non-exist'` | response.fail |
| `split = 'train'` | return `{'bird': 0, 'cat': 1000, 'crab': 2000, 'dog': 3000, 'fish': 4000, 'frog': 5000, 'insect': 6000, 'primate': 7000, 'turtle': 8000}` |

## Get split length `GET /image/<split>`
| param | output |
| -- | -- |
| An invalid split, e.g., `split = 'non-exist'` | response.fail |
| `split = 'train'` | return 9000 |


## Predict `GET /predict/<split>/<image_id>`
| param | output |
| -- | -- |
| An invalid split, e.g., `split = 'non-exist'` | response.fail |
| `image_id` out of bound | response.fail |
| `split = 'train', image_id = 1` | return an array of 3 elements, first two elements both have length 9, third element should be equal to `["/Robustar2/visualize_images/train_1_0.png", "/Robustar2/visualize_images/train_1_1.png", "/Robustar2/visualize_images/train_1_2.png", "/Robustar2/visualize_images/train_1_3.png"]` |


## End-to-end Correctness
TODO

