import React from 'react';

export default function UploadGraphFile(){
    return <div>
        <form action="./logic/uploadFile" method="uploadFile">
            <input type="file" name="myFile"/>
            <input type='submit'/>
        </form>
    </div>
}