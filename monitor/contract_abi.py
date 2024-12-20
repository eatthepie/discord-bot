CONTRACT_ABI = [
  {
    "type": "constructor",
    "inputs": [
      {
        "name": "_vdfContractAddress",
        "type": "address",
        "internalType": "address"
      },
      {
        "name": "_nftPrizeAddress",
        "type": "address",
        "internalType": "address"
      },
      {
        "name": "_feeRecipient",
        "type": "address",
        "internalType": "address"
      }
    ],
    "stateMutability": "nonpayable"
  },
  { "type": "receive", "stateMutability": "payable" },
  {
    "type": "function",
    "name": "BRONZE_PLACE_PERCENTAGE",
    "inputs": [],
    "outputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "DRAW_DELAY_SECURITY_BUFFER",
    "inputs": [],
    "outputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "DRAW_MIN_PRIZE_POOL",
    "inputs": [],
    "outputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "DRAW_MIN_TIME_PERIOD",
    "inputs": [],
    "outputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "EASY_ETHERBALL_MAX",
    "inputs": [],
    "outputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "EASY_MAX",
    "inputs": [],
    "outputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "FEE_MAX_IN_ETH",
    "inputs": [],
    "outputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "FEE_PERCENTAGE",
    "inputs": [],
    "outputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "GOLD_PERCENTAGE",
    "inputs": [],
    "outputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "HARD_ETHERBALL_MAX",
    "inputs": [],
    "outputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "HARD_MAX",
    "inputs": [],
    "outputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "MEDIUM_ETHERBALL_MAX",
    "inputs": [],
    "outputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "MEDIUM_MAX",
    "inputs": [],
    "outputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "SILVER_PLACE_PERCENTAGE",
    "inputs": [],
    "outputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "bronzeTicketCounts",
    "inputs": [
      { "name": "", "type": "uint256", "internalType": "uint256" },
      { "name": "", "type": "bytes32", "internalType": "bytes32" }
    ],
    "outputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "bronzeTicketOwners",
    "inputs": [
      { "name": "", "type": "uint256", "internalType": "uint256" },
      { "name": "", "type": "bytes32", "internalType": "bytes32" },
      { "name": "", "type": "address", "internalType": "address" }
    ],
    "outputs": [{ "name": "", "type": "bool", "internalType": "bool" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "buyTickets",
    "inputs": [
      {
        "name": "tickets",
        "type": "uint256[4][]",
        "internalType": "uint256[4][]"
      }
    ],
    "outputs": [],
    "stateMutability": "payable"
  },
  {
    "type": "function",
    "name": "calculatePayouts",
    "inputs": [{ "name": "gameNumber", "type": "uint256", "internalType": "uint256" }],
    "outputs": [],
    "stateMutability": "nonpayable"
  },
  {
    "type": "function",
    "name": "changeDifficulty",
    "inputs": [],
    "outputs": [],
    "stateMutability": "nonpayable"
  },
  {
    "type": "function",
    "name": "claimPrize",
    "inputs": [{ "name": "gameNumber", "type": "uint256", "internalType": "uint256" }],
    "outputs": [],
    "stateMutability": "nonpayable"
  },
  {
    "type": "function",
    "name": "consecutiveJackpotGames",
    "inputs": [],
    "outputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "consecutiveNonJackpotGames",
    "inputs": [],
    "outputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "currentGameNumber",
    "inputs": [],
    "outputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "feeRecipient",
    "inputs": [],
    "outputs": [{ "name": "", "type": "address", "internalType": "address" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "gameDifficulty",
    "inputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "outputs": [
      {
        "name": "",
        "type": "uint8",
        "internalType": "enum Lottery.Difficulty"
      }
    ],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "gameDrawCompleted",
    "inputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "outputs": [{ "name": "", "type": "bool", "internalType": "bool" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "gameDrawInitiated",
    "inputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "outputs": [{ "name": "", "type": "bool", "internalType": "bool" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "gameDrawnBlock",
    "inputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "outputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "gamePayouts",
    "inputs": [
      { "name": "", "type": "uint256", "internalType": "uint256" },
      { "name": "", "type": "uint256", "internalType": "uint256" }
    ],
    "outputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "gamePrizePool",
    "inputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "outputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "gameRandomBlock",
    "inputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "outputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "gameRandomValue",
    "inputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "outputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "gameStartBlock",
    "inputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "outputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "gameVDFValid",
    "inputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "outputs": [{ "name": "", "type": "bool", "internalType": "bool" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "gameWinningNumbers",
    "inputs": [
      { "name": "", "type": "uint256", "internalType": "uint256" },
      { "name": "", "type": "uint256", "internalType": "uint256" }
    ],
    "outputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "getBasicGameInfo",
    "inputs": [
      { "name": "startGameId", "type": "uint256", "internalType": "uint256" },
      { "name": "endGameId", "type": "uint256", "internalType": "uint256" }
    ],
    "outputs": [
      {
        "name": "gameInfos",
        "type": "tuple[]",
        "internalType": "struct Lottery.GameBasicInfo[]",
        "components": [
          { "name": "gameId", "type": "uint256", "internalType": "uint256" },
          {
            "name": "status",
            "type": "uint8",
            "internalType": "enum Lottery.GameStatus"
          },
          {
            "name": "prizePool",
            "type": "uint256",
            "internalType": "uint256"
          },
          {
            "name": "numberOfWinners",
            "type": "uint256",
            "internalType": "uint256"
          },
          {
            "name": "winningNumbers",
            "type": "uint256[4]",
            "internalType": "uint256[4]"
          }
        ]
      }
    ],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "getCurrentGameInfo",
    "inputs": [],
    "outputs": [
      { "name": "gameNumber", "type": "uint256", "internalType": "uint256" },
      {
        "name": "difficulty",
        "type": "uint8",
        "internalType": "enum Lottery.Difficulty"
      },
      { "name": "prizePool", "type": "uint256", "internalType": "uint256" },
      { "name": "drawTime", "type": "uint256", "internalType": "uint256" },
      {
        "name": "timeUntilDraw",
        "type": "uint256",
        "internalType": "uint256"
      }
    ],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "getDetailedGameInfo",
    "inputs": [{ "name": "gameId", "type": "uint256", "internalType": "uint256" }],
    "outputs": [
      {
        "name": "",
        "type": "tuple",
        "internalType": "struct Lottery.GameDetailedInfo",
        "components": [
          { "name": "gameId", "type": "uint256", "internalType": "uint256" },
          {
            "name": "status",
            "type": "uint8",
            "internalType": "enum Lottery.GameStatus"
          },
          {
            "name": "prizePool",
            "type": "uint256",
            "internalType": "uint256"
          },
          {
            "name": "numberOfWinners",
            "type": "uint256",
            "internalType": "uint256"
          },
          {
            "name": "goldWinners",
            "type": "uint256",
            "internalType": "uint256"
          },
          {
            "name": "silverWinners",
            "type": "uint256",
            "internalType": "uint256"
          },
          {
            "name": "bronzeWinners",
            "type": "uint256",
            "internalType": "uint256"
          },
          {
            "name": "winningNumbers",
            "type": "uint256[4]",
            "internalType": "uint256[4]"
          },
          {
            "name": "difficulty",
            "type": "uint8",
            "internalType": "enum Lottery.Difficulty"
          },
          {
            "name": "drawInitiatedBlock",
            "type": "uint256",
            "internalType": "uint256"
          },
          {
            "name": "randaoBlock",
            "type": "uint256",
            "internalType": "uint256"
          },
          {
            "name": "randaoValue",
            "type": "uint256",
            "internalType": "uint256"
          },
          {
            "name": "payouts",
            "type": "uint256[3]",
            "internalType": "uint256[3]"
          }
        ]
      }
    ],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "getUserGameWinnings",
    "inputs": [
      { "name": "gameNumber", "type": "uint256", "internalType": "uint256" },
      { "name": "user", "type": "address", "internalType": "address" }
    ],
    "outputs": [
      { "name": "goldWin", "type": "bool", "internalType": "bool" },
      { "name": "silverWin", "type": "bool", "internalType": "bool" },
      { "name": "bronzeWin", "type": "bool", "internalType": "bool" },
      { "name": "totalPrize", "type": "uint256", "internalType": "uint256" },
      { "name": "claimed", "type": "bool", "internalType": "bool" }
    ],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "goldTicketCounts",
    "inputs": [
      { "name": "", "type": "uint256", "internalType": "uint256" },
      { "name": "", "type": "bytes32", "internalType": "bytes32" }
    ],
    "outputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "goldTicketOwners",
    "inputs": [
      { "name": "", "type": "uint256", "internalType": "uint256" },
      { "name": "", "type": "bytes32", "internalType": "bytes32" },
      { "name": "", "type": "address", "internalType": "address" }
    ],
    "outputs": [{ "name": "", "type": "bool", "internalType": "bool" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "hasClaimedNFT",
    "inputs": [
      { "name": "", "type": "uint256", "internalType": "uint256" },
      { "name": "", "type": "address", "internalType": "address" }
    ],
    "outputs": [{ "name": "", "type": "bool", "internalType": "bool" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "hasUserWon",
    "inputs": [
      { "name": "gameNumber", "type": "uint256", "internalType": "uint256" },
      { "name": "user", "type": "address", "internalType": "address" }
    ],
    "outputs": [{ "name": "hasWon", "type": "bool", "internalType": "bool" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "initiateDraw",
    "inputs": [],
    "outputs": [],
    "stateMutability": "nonpayable"
  },
  {
    "type": "function",
    "name": "lastDrawTime",
    "inputs": [],
    "outputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "mintWinningNFT",
    "inputs": [{ "name": "gameNumber", "type": "uint256", "internalType": "uint256" }],
    "outputs": [],
    "stateMutability": "nonpayable"
  },
  {
    "type": "function",
    "name": "newDifficulty",
    "inputs": [],
    "outputs": [
      {
        "name": "",
        "type": "uint8",
        "internalType": "enum Lottery.Difficulty"
      }
    ],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "newDifficultyGame",
    "inputs": [],
    "outputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "newTicketPrice",
    "inputs": [],
    "outputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "newTicketPriceGameNumber",
    "inputs": [],
    "outputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "newVDFContract",
    "inputs": [],
    "outputs": [{ "name": "", "type": "address", "internalType": "address" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "newVDFContractGameNumber",
    "inputs": [],
    "outputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "nftPrize",
    "inputs": [],
    "outputs": [{ "name": "", "type": "address", "internalType": "contract NFTPrize" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "owner",
    "inputs": [],
    "outputs": [{ "name": "", "type": "address", "internalType": "address" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "playerTicketCount",
    "inputs": [
      { "name": "", "type": "address", "internalType": "address" },
      { "name": "", "type": "uint256", "internalType": "uint256" }
    ],
    "outputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "prizesClaimed",
    "inputs": [
      { "name": "", "type": "uint256", "internalType": "uint256" },
      { "name": "", "type": "address", "internalType": "address" }
    ],
    "outputs": [{ "name": "", "type": "bool", "internalType": "bool" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "renounceOwnership",
    "inputs": [],
    "outputs": [],
    "stateMutability": "nonpayable"
  },
  {
    "type": "function",
    "name": "setFeeRecipient",
    "inputs": [
      {
        "name": "_newFeeRecipient",
        "type": "address",
        "internalType": "address"
      }
    ],
    "outputs": [],
    "stateMutability": "nonpayable"
  },
  {
    "type": "function",
    "name": "setNewVDFContract",
    "inputs": [
      {
        "name": "_newVDFContract",
        "type": "address",
        "internalType": "address"
      }
    ],
    "outputs": [],
    "stateMutability": "nonpayable"
  },
  {
    "type": "function",
    "name": "setRandom",
    "inputs": [{ "name": "gameNumber", "type": "uint256", "internalType": "uint256" }],
    "outputs": [],
    "stateMutability": "nonpayable"
  },
  {
    "type": "function",
    "name": "setTicketPrice",
    "inputs": [{ "name": "_newPrice", "type": "uint256", "internalType": "uint256" }],
    "outputs": [],
    "stateMutability": "nonpayable"
  },
  {
    "type": "function",
    "name": "silverTicketCounts",
    "inputs": [
      { "name": "", "type": "uint256", "internalType": "uint256" },
      { "name": "", "type": "bytes32", "internalType": "bytes32" }
    ],
    "outputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "silverTicketOwners",
    "inputs": [
      { "name": "", "type": "uint256", "internalType": "uint256" },
      { "name": "", "type": "bytes32", "internalType": "bytes32" },
      { "name": "", "type": "address", "internalType": "address" }
    ],
    "outputs": [{ "name": "", "type": "bool", "internalType": "bool" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "submitVDFProof",
    "inputs": [
      { "name": "gameNumber", "type": "uint256", "internalType": "uint256" },
      {
        "name": "v",
        "type": "tuple[]",
        "internalType": "struct BigNumber[]",
        "components": [
          { "name": "val", "type": "bytes", "internalType": "bytes" },
          { "name": "bitlen", "type": "uint256", "internalType": "uint256" }
        ]
      },
      {
        "name": "y",
        "type": "tuple",
        "internalType": "struct BigNumber",
        "components": [
          { "name": "val", "type": "bytes", "internalType": "bytes" },
          { "name": "bitlen", "type": "uint256", "internalType": "uint256" }
        ]
      }
    ],
    "outputs": [],
    "stateMutability": "nonpayable"
  },
  {
    "type": "function",
    "name": "ticketPrice",
    "inputs": [],
    "outputs": [{ "name": "", "type": "uint256", "internalType": "uint256" }],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "transferOwnership",
    "inputs": [{ "name": "newOwner", "type": "address", "internalType": "address" }],
    "outputs": [],
    "stateMutability": "nonpayable"
  },
  {
    "type": "function",
    "name": "uint256ToBigNumber",
    "inputs": [{ "name": "input", "type": "uint256", "internalType": "uint256" }],
    "outputs": [
      { "name": "val", "type": "bytes", "internalType": "bytes" },
      { "name": "bitlen", "type": "uint256", "internalType": "uint256" }
    ],
    "stateMutability": "pure"
  },
  {
    "type": "function",
    "name": "vdfContract",
    "inputs": [],
    "outputs": [
      {
        "name": "",
        "type": "address",
        "internalType": "contract VDFPietrzak"
      }
    ],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "verifyPastGameVDF",
    "inputs": [
      { "name": "gameNumber", "type": "uint256", "internalType": "uint256" },
      {
        "name": "v",
        "type": "tuple[]",
        "internalType": "struct BigNumber[]",
        "components": [
          { "name": "val", "type": "bytes", "internalType": "bytes" },
          { "name": "bitlen", "type": "uint256", "internalType": "uint256" }
        ]
      },
      {
        "name": "y",
        "type": "tuple",
        "internalType": "struct BigNumber",
        "components": [
          { "name": "val", "type": "bytes", "internalType": "bytes" },
          { "name": "bitlen", "type": "uint256", "internalType": "uint256" }
        ]
      }
    ],
    "outputs": [
      {
        "name": "calculatedNumbers",
        "type": "uint256[4]",
        "internalType": "uint256[4]"
      },
      { "name": "isValid", "type": "bool", "internalType": "bool" }
    ],
    "stateMutability": "view"
  },
  {
    "type": "event",
    "name": "DifficultyChanged",
    "inputs": [
      {
        "name": "gameNumber",
        "type": "uint256",
        "indexed": False,
        "internalType": "uint256"
      },
      {
        "name": "newDifficulty",
        "type": "uint8",
        "indexed": False,
        "internalType": "enum Lottery.Difficulty"
      }
    ],
    "anonymous": False
  },
  {
    "type": "event",
    "name": "DrawInitiated",
    "inputs": [
      {
        "name": "gameNumber",
        "type": "uint256",
        "indexed": False,
        "internalType": "uint256"
      },
      {
        "name": "targetSetBlock",
        "type": "uint256",
        "indexed": False,
        "internalType": "uint256"
      }
    ],
    "anonymous": False
  },
  {
    "type": "event",
    "name": "ExcessPrizePoolTransferred",
    "inputs": [
      {
        "name": "fromGame",
        "type": "uint256",
        "indexed": False,
        "internalType": "uint256"
      },
      {
        "name": "toGame",
        "type": "uint256",
        "indexed": False,
        "internalType": "uint256"
      },
      {
        "name": "amount",
        "type": "uint256",
        "indexed": False,
        "internalType": "uint256"
      }
    ],
    "anonymous": False
  },
  {
    "type": "event",
    "name": "FeeRecipientChanged",
    "inputs": [
      {
        "name": "newFeeRecipient",
        "type": "address",
        "indexed": False,
        "internalType": "address"
      }
    ],
    "anonymous": False
  },
  {
    "type": "event",
    "name": "GamePrizePayoutInfo",
    "inputs": [
      {
        "name": "gameNumber",
        "type": "uint256",
        "indexed": False,
        "internalType": "uint256"
      },
      {
        "name": "goldPrize",
        "type": "uint256",
        "indexed": False,
        "internalType": "uint256"
      },
      {
        "name": "silverPrize",
        "type": "uint256",
        "indexed": False,
        "internalType": "uint256"
      },
      {
        "name": "bronzePrize",
        "type": "uint256",
        "indexed": False,
        "internalType": "uint256"
      }
    ],
    "anonymous": False
  },
  {
    "type": "event",
    "name": "NFTMinted",
    "inputs": [
      {
        "name": "winner",
        "type": "address",
        "indexed": True,
        "internalType": "address"
      },
      {
        "name": "tokenId",
        "type": "uint256",
        "indexed": True,
        "internalType": "uint256"
      },
      {
        "name": "gameNumber",
        "type": "uint256",
        "indexed": True,
        "internalType": "uint256"
      }
    ],
    "anonymous": False
  },
  {
    "type": "event",
    "name": "OwnershipTransferred",
    "inputs": [
      {
        "name": "previousOwner",
        "type": "address",
        "indexed": True,
        "internalType": "address"
      },
      {
        "name": "newOwner",
        "type": "address",
        "indexed": True,
        "internalType": "address"
      }
    ],
    "anonymous": False
  },
  {
    "type": "event",
    "name": "PrizeClaimed",
    "inputs": [
      {
        "name": "gameNumber",
        "type": "uint256",
        "indexed": False,
        "internalType": "uint256"
      },
      {
        "name": "player",
        "type": "address",
        "indexed": False,
        "internalType": "address"
      },
      {
        "name": "amount",
        "type": "uint256",
        "indexed": False,
        "internalType": "uint256"
      }
    ],
    "anonymous": False
  },
  {
    "type": "event",
    "name": "RandomSet",
    "inputs": [
      {
        "name": "gameNumber",
        "type": "uint256",
        "indexed": False,
        "internalType": "uint256"
      },
      {
        "name": "random",
        "type": "uint256",
        "indexed": False,
        "internalType": "uint256"
      }
    ],
    "anonymous": False
  },
  {
    "type": "event",
    "name": "TicketPriceChangeScheduled",
    "inputs": [
      {
        "name": "newPrice",
        "type": "uint256",
        "indexed": False,
        "internalType": "uint256"
      },
      {
        "name": "effectiveGameNumber",
        "type": "uint256",
        "indexed": False,
        "internalType": "uint256"
      }
    ],
    "anonymous": False
  },
  {
    "type": "event",
    "name": "TicketPurchased",
    "inputs": [
      {
        "name": "player",
        "type": "address",
        "indexed": True,
        "internalType": "address"
      },
      {
        "name": "gameNumber",
        "type": "uint256",
        "indexed": False,
        "internalType": "uint256"
      },
      {
        "name": "numbers",
        "type": "uint256[3]",
        "indexed": False,
        "internalType": "uint256[3]"
      },
      {
        "name": "etherball",
        "type": "uint256",
        "indexed": False,
        "internalType": "uint256"
      }
    ],
    "anonymous": False
  },
  {
    "type": "event",
    "name": "TicketsPurchased",
    "inputs": [
      {
        "name": "player",
        "type": "address",
        "indexed": True,
        "internalType": "address"
      },
      {
        "name": "gameNumber",
        "type": "uint256",
        "indexed": False,
        "internalType": "uint256"
      },
      {
        "name": "ticketCount",
        "type": "uint256",
        "indexed": False,
        "internalType": "uint256"
      }
    ],
    "anonymous": False
  },
  {
    "type": "event",
    "name": "VDFProofSubmitted",
    "inputs": [
      {
        "name": "submitter",
        "type": "address",
        "indexed": True,
        "internalType": "address"
      },
      {
        "name": "gameNumber",
        "type": "uint256",
        "indexed": False,
        "internalType": "uint256"
      }
    ],
    "anonymous": False
  },
  {
    "type": "event",
    "name": "WinningNumbersSet",
    "inputs": [
      {
        "name": "gameNumber",
        "type": "uint256",
        "indexed": True,
        "internalType": "uint256"
      },
      {
        "name": "number1",
        "type": "uint256",
        "indexed": False,
        "internalType": "uint256"
      },
      {
        "name": "number2",
        "type": "uint256",
        "indexed": False,
        "internalType": "uint256"
      },
      {
        "name": "number3",
        "type": "uint256",
        "indexed": False,
        "internalType": "uint256"
      },
      {
        "name": "etherball",
        "type": "uint256",
        "indexed": False,
        "internalType": "uint256"
      }
    ],
    "anonymous": False
  },
  {
    "type": "error",
    "name": "OwnableInvalidOwner",
    "inputs": [{ "name": "owner", "type": "address", "internalType": "address" }]
  },
  {
    "type": "error",
    "name": "OwnableUnauthorizedAccount",
    "inputs": [{ "name": "account", "type": "address", "internalType": "address" }]
  },
  { "type": "error", "name": "ReentrancyGuardReentrantCall", "inputs": [] }
]
