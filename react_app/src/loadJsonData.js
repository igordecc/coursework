/* 
little programm
load data from DataUrl
make collection
then return data out
 */

import React from 'react';

const DataURL = `http://localhost:5000/`

function loadJsonData() {
    fetch(DataURL).
    then(result => result.json()).
    then(data => console.log(data))
    
    return 
}

export default loadJsonData;