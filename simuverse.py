import streamlit as st
import os
from PIL import Image
import open3d as o3d

st.set_page_config(layout='wide')

st.title('SimuVerse 3D Virtual Try-on App')
st.write('This app enables virtual try-on given input images of a clothing item and person.')

st.header('Input')

col1, col2 = st.columns((1,1))

col1.subheader('Clothing')
clothing = col1.file_uploader('Upload Cloth Image', type=['jpg'])
if clothing is not None:
    col1.image(clothing)

col2.subheader('Person')
person = col2.file_uploader('Upload Person Image', type=['png'])
if person is not None:
    col2.image(person)

if st.button('Run Virtual Try-On'):
    if (clothing is None) or (person is None):
        st.write('**Error**: input images not provided!')
    else:
        st.header('Output')
        # saving images in directory
        with open('./m3d-vton/input_data/cloth/cloth@1=cloth_front.jpg', 'wb') as f:
            f.write((clothing).getbuffer())
        with open('./m3d-vton/input_data/image/person@1=person_whole_front.png', 'wb') as f:
            f.write((person).getbuffer())
        # running inference
        # os.system("python3 inference.py")
        output = Image.open('./m3d-vton/output_data/person@1=person_whole_front_result_2d.png')
        st.image(output)

        # PCD
        pcd = o3d.io.read_point_cloud('./m3d-vton/output_data/person@1=person.ply')
        # normal estimation
        pcd.estimate_normals()
        pcd.orient_normals_consistent_tangent_plane(100)
        # poisson surface reconstruction
        mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=9)
        st.write(o3d.visualization.draw_geometries([mesh]))
        
