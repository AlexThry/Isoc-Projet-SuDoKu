// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

contract SudokuSolver {
    struct Participant {
        uint256 attempts;
    }

    mapping(address => Participant) public participants;
    address[] public participantAddresses;
    mapping(bytes32 => bool) public bloomFilterHashes;
    address public owner;
    uint256 public totalAttempts;

    constructor() {
        owner = msg.sender;
    }

    function participate(uint256 attempts, bytes32 bloomFilterHash) public {
        require(bloomFilterHashes[bloomFilterHash] == false, "Ce hash de filtre de Bloom a déjà été soumis.");
        if (participants[msg.sender].attempts == 0) {
            participantAddresses.push(msg.sender);
        }
        participants[msg.sender].attempts += attempts;
        totalAttempts += attempts;
        bloomFilterHashes[bloomFilterHash] = true;
    }

    function distributeReward() public payable {
        require(msg.sender == owner, "Seul le propriétaire du smart contract peut distribuer la récompense.");
        require(msg.value >= totalAttempts, "Le contrat n'a pas assez de pEth pour payer la récompense.");
        for(uint256 i = 0; i < participantAddresses.length; i++) {
            address participantAddress = participantAddresses[i];
            payable(participantAddress).transfer((msg.value * participants[participantAddress].attempts) / totalAttempts);
        }
    }
}
