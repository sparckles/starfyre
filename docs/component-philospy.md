## Component Philosophy

Every component in Starfyre will be a stateless component. This means that the component will not have any state of its own.

Should there be a need for a stateful component, the state will be treated like a unique entity.

Just by including a state in the component, the component will be subscribed to the state. This means that the component will be re-rendered every time the state changes.

The state doesn't have to be a global state. It can be a local state too. We don't need to do prop drilling to pass the state to the component. The component will be subscribed to the state, and it will be re-rendered every time the state changes.
