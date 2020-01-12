import React from 'react';
const _ = require('underscore');

export default function Reload(props){
  // return <button onClick={handleReloadOscillatorsData}>Reload</button>
  return <button onClick={props.onClick}>Reload</button>
};