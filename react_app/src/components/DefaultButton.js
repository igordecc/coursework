import React from 'react';

export default function DefaultButton(props){
    //console.log(props.buttonLable)
    return <button onClick={props.onClick}>{props.buttonLable}</button>
  };