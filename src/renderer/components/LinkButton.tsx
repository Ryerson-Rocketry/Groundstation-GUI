import React from 'react';

type LinkButton = {
    link: string
    buttonName: string
}

function LinkEvent(link: string){
  return location.href= link;
}
  
export const LinkButton = ({ link, buttonName }: LinkButton) => <aside>
  <button onClick={() => LinkEvent(link)}> {buttonName} </button>
</aside>
  
