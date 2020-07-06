pragma solidity ^0.5.16;

contract FoodSafety
{
    struct Record {
        string sensorId;
        int256 temperature;
        int256 humidity;
        string timestamp;
    }

    uint public numRecords;
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
        numRecords = 0;

        emit StateChanged('Request');
    }
    function SetRecord(string memory sensorId, int256 temperature, int256 humidity, string memory timestamp) public returns (bool) {
        Record memory r;
        r.sensorId = sensorId;
        r.temperature = temperature;
        r.humidity = humidity;
        r.timestamp = timestamp;
        if (isValid(r)) {
            records.push(r);
            numRecords++;
            return (true);
        } else {
            setInvalid(r);
            return (false);
        }
    }
    function isValid(Record memory r) private pure returns (bool) {
        int256 minTemp = -30;
        int256 maxTemp = 32;
        int minHumidity = -50;
        int maxHumidity = 99;
        if (r.temperature < minTemp || r.temperature > maxTemp) {
            return false;
        }
        if (r.humidity < minHumidity || r.humidity > maxHumidity) {
            return false;
        }
        return true;
    }
    function setInvalid(Record memory r) private {
        State = StateType.NonCompliant;
        emit StateChanged("HORRIBLE!!!!!!");
    }
    function GetRecordCount() public view  returns (uint) {
        return numRecords;
    }
    function GetRecordByIndex(uint index) public view returns (string memory, int256, int256, string memory) {
        if (index > numRecords) {
            revert("Error - the index exceeds the number of records");
        }
        Record memory r = records[index];
        return (r.sensorId, r.temperature, r.humidity, r.timestamp);
    }
    function GetContractState() public view returns (StateType) {
        return State;
    }
}