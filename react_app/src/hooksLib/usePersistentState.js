import React from 'react';
function usePersistentState(init, itemName='') {
    const [value, setValue] = React.useState(
      JSON.parse(localStorage.getItem(itemName)) || init
    )
    React.useEffect(() => {
      localStorage.setItem(itemName, JSON.stringify(value))
    })
    return [value, setValue]
  }

export default usePersistentState;