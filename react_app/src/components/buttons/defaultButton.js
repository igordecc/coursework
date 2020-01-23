import React from 'react';

export default function DefaultButton(props){
    console.log(props.value)
    console.log(props.buttonText)
    
    return <button onClick={props.onClick}>{props.buttonText}</button>
  };