import * as React from 'react';

export default class Instruction extends React.Component<any> {
    render() {
	return (<div className="instruction">
	        {this.props.instructions}
	        </div>);
    }
};
