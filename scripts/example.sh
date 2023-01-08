# setup
# ./robustar.sh -m setup -a cuda11.1-0.0.1-beta \

## Running on cuda11.1 (For linux users)
# ./robustar.sh -m run -p 8081 \
# -a "cuda11.1-0.1.0-beta" \
# -t "/Robustar2/dataset/train" \
# -e "/Robustar2/dataset/test" \
# -r "/Robustar2/dataset/paired" \
# -d "/Robustar2/dataset/test" \
# -i "/Robustar2/influence_images" \
# -o "/Robustar2/configs.json" \
# -c "/Robustar2/checkpoints" 
# -g "/Robustar2/generated" 

# Running on cpu (For windows users)
./robustar.sh \
-m run \
-a 0.1_fixes_a3e3fe0 \
-p 8080 \
-t C:\\Robustar2\\dataset\\train \
-e C:\\Robustar2\\dataset\\test \
-r C:\\Robustar2\\dataset\\paired \
-d C:\\Robustar2\\dataset\\test \
-i C:\\Robustar2\\influence_images \
-c C:\\Robustar2\\checkpoints \
-g C:\\Robustar2\\generated \
-o C:\\Robustar2\\configs.json

