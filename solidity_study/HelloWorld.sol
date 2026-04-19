// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract HelloWorld {
    string public greeting = "Hello, Coco Commander!";

    function setGreeting(string memory _newGreeting) public {
        greeting = _newGreeting;
    }
// 숫자를 저장할 변수 하나 추가!
uint256 public count = 0;

// 숫자를 1씩 올리는 함수!
function addCount() public {
    count = count + 1;
}
}
