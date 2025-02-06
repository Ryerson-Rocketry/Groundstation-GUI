import React from 'react';

type CardProps = { //Think of this like a function declaration like in a header file in c
    title: string,
    paragraph: string
}
  
  export const Card = ({ title, paragraph }: CardProps) => <aside>
    <h2>{ title }</h2>
    <p>
      { paragraph }
    </p>
  </aside>
  
// const el = <Card title="Welcome!" paragraph="To this example" /> //example of a component declaration