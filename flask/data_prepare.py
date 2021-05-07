import os
import pandas as pd

base_dir = 'corona_dataset/Coronahack-Chest-XRay-Dataset/Coronahack-Chest-XRay-Dataset'
train_dir = os.path.join(base_dir, 'train')
test_dir = os.path.join(base_dir, 'test')

df = pd.read_csv('corona_dataset/Chest_xray_Corona_Metadata.csv')
df.head()

print(df['Label_1_Virus_category'].value_counts())
print('='*50)
print(df['Label_2_Virus_category'].value_counts())
print(df['Label'].value_counts())

# Augment dataset
train_data = df[df['Dataset_type']=='TRAIN']
test_data = df[df['Dataset_type']=='TEST']

print('Train shape: ', train_data.shape)
print('Test Shape: ', test_data.shape)

pics_with_covid = train_data[train_data['Label_2_Virus_category'] == 'COVID-19']


#show sample image
# samp_img1 = PIL.Image.open(os.path.join(train_dir, pics_with_covid['X_ray_image_name'].iloc[8]))
# samp_img2 = PIL.Image.open(os.path.join(train_dir, pics_with_covid['X_ray_image_name'].iloc[15]))
# fig, ax =plt.subplots(1,2, figsize=(10,5))
# ax[0].imshow(samp_img1);
# ax[1].imshow(samp_img2);

final_train_data = train_data


final_train_data['class'] = final_train_data.Label_2_Virus_category.apply(lambda x: 'positive' if x=='COVID-19' else 'negative')
test_data['class'] = test_data.Label_2_Virus_category.apply(lambda x: 'positive' if x=='COVID-19' else 'negative')

final_train_data['target'] = final_train_data.Label_2_Virus_category.apply(lambda x: 1 if x=='COVID-19' else 0)
test_data['target'] = test_data.Label_2_Virus_category.apply(lambda x: 1 if x=='COVID-19' else 0)


# Take only the columns we need.
final_train_data = final_train_data[['X_ray_image_name', 'class', 'target', 'Label_2_Virus_category']]
final_test_data = test_data[['X_ray_image_name', 'class', 'target']]

# Tensorflow ImageDataGenerator for augmentation
datagen =  ImageDataGenerator(
  shear_range=0.2,
  zoom_range=0.2,
  # rotation_range=5,
  # width_shift_range=0.2,
  # height_shift_range=0.2,
  # zca_whitening
  # brighhtness_range
  horizontal_flip=True
)
# todo: don't apply on only covid images. 
# Check out datagen.flow_from_Directory

# Converts dataset imgs to arrays by div / 255
def read_img(filename, size, path):

    img = image.load_img(os.path.join(path, filename), target_size=size)

    # Use img_to_array() built in method
    img = image.img_to_array(img) / 255
    return img

# Take slice of dataframe of only covid19 images
corona_df = final_train_data[final_train_data['Label_2_Virus_category'] == 'COVID-19']
with_corona_augmented = []

# Augmentation function, process in batches
def augment(name):
    img = read_img(name, (mv, mv), train_dir)
    i = 0
    for batch in tqdm(datagen.flow(tf.expand_dims(img, 0), batch_size=32)):
        with_corona_augmented.append(tf.squeeze(batch).numpy())
        if i == 20:
            break
        i =i+1

# Apply the actual augmentation to the slices with covid19
corona_df['X_ray_image_name'].apply(augment)

# Extract images from traing data and test data, then convert them as array
train_arrays = [] 
final_train_data['X_ray_image_name'].apply(lambda x: train_arrays.append(read_img(x, (mv,mv), train_dir)))

test_arrays = []
final_test_data['X_ray_image_name'].apply(lambda x: test_arrays.append(read_img(x, (mv,mv), test_dir)))

print(len(train_arrays))
print(len(test_arrays))

print("Test")