# DEBUG
docker run -itd --name robustar  \
-p 127.0.0.1:8080:80 \
-p 127.0.0.1:6848:8000 \
--mount type=bind,source=C:\\Robustar2\\dataset\\train,target=/Robustar2/dataset/train \
--mount type=bind,source=C:\\Robustar2\\dataset\\test,target=/Robustar2/dataset/test \
--mount type=bind,source=C:\\Robustar2\\influence_images,target=/Robustar2/influence_images \
--mount type=bind,source=C:\\Robustar2\\checkpoints,target=/Robustar2/checkpoint_images \
-v C:\\Robustar2\\configs.json:/Robustar2/configs.json \
"paulcccccch/robustar:cpu-0.0.1-beta"

# docker cp  C:\\Robustar2\\configs.json robustar:/Robustar2/configs.json 

# docker start robustar
# docker run -itd --name robustar -p 127.0.0.1:8080:80 -p 127.0.0.1:6848:8000 --mount type=bind,source=C:\\Robustar2\\dataset\\train,target=/Robustar2/dataset/train --mount type=bind,source=C:\\Robustar2\\dataset\\test,target=/Robustar2/dataset/test --mount type=bind,source=C:\\Robustar2\\influence_images,target=/Robustar2/influence_images --mount type=bind,source=C:\\Robustar2\\checkpoints,target=/Robustar2/checkpoint_images -v C:\\Robustar2\\configs.json:/Robustar2/configs.json "paulcccccch/robustar:cpu-0.0.1-beta" 