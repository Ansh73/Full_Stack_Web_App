import React, { Component } from 'react';
export default class Home extends Component {
    render() {
       return (
	   <div className = 'myform'>
			<h1>Enter the DNA Sequence to search for</h1>
			<form action = "http://localhost:5000/search" method = "POST">
			<input type = "text" name = "Name" />
			<b><a href = '/logout'>click here to log out</a></b>
			</form>
		</div>
       )
    }
}