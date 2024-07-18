# Depth images project

### Task description
Csv file that contains image data referenced by the column depth. The rest of columns (200) represent image pixel values from 0 to 255 at each depth.
The challenge consists on the following requirements:

·       The image size is relatively big. Hence, there is a need to resize the image width to 150 instead of 200.

·       The resized image has to be stored in a database.

·       An API is required to request image frames based on depth_min and depth_max.

·       Apply a custom color map to the generated frames.

·       The solution should be based on Python.

# Start
### 1. Install docker and docker-compose
### 2. Create env file
````
cp .env.sample .env
````
### 3. Run command
````
make run
````

# How to use
#### Open url - http://127.0.0.1:8000/docs and use swagger documentation.

# For uploading csv file run
````
make upload_csv
````
If you want to upload file with different name, you can add file to the script folder, build image with `make build` command and run command like this
```
docker exec depth_images_backend  python scripts/parse_csv.py --file_path "/home/app/scripts/{your_file_name}.csv"
```
ps. don't forget to change `your_file_name`

# Tests
```
make test
```
