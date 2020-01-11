import React from 'react';
import usePersistentState from './usePersistentState';
function usePersistentData(init){
    const [data, setData] = usePersistentState(init, 'osc-data')
    
    return [data, setData]
  }

export default usePersistentData;