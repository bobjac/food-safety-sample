pragma solidity ^0.5.0;

contract FoodSafety
{
    struct Record {
        string sensorId;
        int256 temperature;
        int256 humidity;
        string timestamp;
    }

    Record[] public records;

    address private owner;

     //Set of States
    enum StateType { Compliant, NonCompliant }

    //List of properties
    StateType public  State;


    event StateChanged(string stateData);

    // constructor function
    constructor() public
    {
        owner = msg.sender;

        emit StateChanged('Request');
    }

    function SetRecord(string memory sensorId, int256 temperature, int256 humidity, string memory timestamp) public
    {
        Record memory r;
        r.sensorId = sensorId;
        r.temperature = temperature;
        r.humidity = humidity;
        r.timestamp = timestamp;
        records.push(r);
    }
}