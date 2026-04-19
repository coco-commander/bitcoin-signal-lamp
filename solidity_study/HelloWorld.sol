// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract HelloWorld {
    string public greeting = "Hello, Coco Commander!";

    function setGreeting(string memory _newGreeting) public {
        greeting = _newGreeting;
    }
}
