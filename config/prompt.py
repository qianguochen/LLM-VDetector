

prompt_system = "You are a smart contract security expert, skilled in remediating Solidity vulnerabilities through code refactoring and best practice implementation. "

prompt_start = "USER:You are a smart contract auditor, You will be asked questions related to code properties. You can mimic answering them in the background five times and provide me with the most frequently appearing answer.Only need one. Furthermore, please strictly adhere to the output format specified in the question;"
prompt_start_ast = "USER:You are a smart contract auditor,skilled at analyzing the AST (Abstract Syntax Tree) compiled by Solidity to identify security vulnerabilities. You will be asked questions related to code properties. You can mimic answering them in the background five times and provide me with the most frequently appearing answer.Only need one. Furthermore, please strictly adhere to the output format specified in the question;"
prompt_start_ast_source_code = "USER:You are a smart contract auditor,skilled at analyzing Solidity source code and its compiled AST (Abstract Syntax Tree) to identify security vulnerabilities.  You will be provided with source code and may be asked about specific code properties or vulnerabilities. You can mimic answering them in the background five times and provide me with the most frequently appearing answer.Only need one. Furthermore, please strictly adhere to the output format specified in the question;Current Audit Task: 1.Provided Materials: Solidity Source Code & AST Analysis; 2.Vulnerability to Analyze:"
prompt_start_fix = "You will be provided with source code, precise vulnerability locations, and detailed vulnerability type descriptions. You can mimic proposing solutions in the background five times and provide me with the most effective remediation approach. Only need one. Furthermore, please strictly adhere to the output format specified in the question;Current Audit Task:"

prompt_vulnerable_type = {
    "Authorization_through_tx.origin": "Analyze the possible risks of Authorization through tx.origin vulnerability in these codes: ",
    "Delegatecall_to_Untrusted_Callee": "Analyze the possible risks of Delegatecall to Untrusted Callee vulnerability in these codes: ",
    "Integer_Overflow_and_Underflow": "Analyze the possible risks of Integer Overflow and Underflow vulnerability in these codes(Please ignore the impact of solidity compiler versions 0.8.0 and above on the source code): ",
    "Presence_of_unused_variables": "Analyze the possible risks of Presence of unused variables vulnerability in these codes: ",
    "Reentrancy": "Analyze the possible risks of Reentrancy vulnerability in these codes: ",
    "Transaction_Order_Dependence": "Analyze the possible risks of Transaction Order Dependence vulnerability in these codes: ",
    "Unchecked_Call_Return_Value": "Analyze the possible risks of Unchecked Call Return Value vulnerability in these codes: ",
    "Unprotected_Ether_Withdrawal": "Analyze the possible risks of Unprotected Ether Withdrawal vulnerability in these codes: ",
    "Assert_Violation": "Analyze the possible risks of Assert Violation vulnerability in these codes: ",
    "Block_values_as_a_proxy_for_time": "Analyze the possible risks of Block values as a proxy for time vulnerability in these codes: ",
    "Code_With_No_Effects": "Analyze the possible risks of Code With No Effects vulnerability in these codes: ",
    "DoS_with_Failed_Call": "Analyze the possible risks of DoS with Failed Call vulnerability in these codes: ",
    "DoS_With_Block_Gas_Limit": "Analyze the possible risks of DoS With Block Gas Limit vulnerability in these codes: ",
    "Floating_Pragma": "Analyze the possible risks of Floating Pragma vulnerability in these codes: \n",
    "Function_Default_Visibility": "Analyze the possible risks of Function Default Visibility vulnerability in these codes: ",
    "Hash_Collisions_With_Multiple_Variable_Length_Arguments": "Analyze the possible risks of Hash Collisions With Multiple Variable Length Arguments vulnerability in these codes: ",
    "Incorrect_Inheritance_Order": "Analyze the possible risks of Incorrect Inheritance Order vulnerability in these codes: ",
    "Insufficient_Gas_Griefing": "Analyze the possible risks of Insufficient Gas Griefing vulnerability in these codes: ",
    "Lack_of_Proper_Signature_Verification": "Analyze the possible risks of Lack of Proper Signature Verification vulnerability in these codes: ",
    "Missing_Protection_against_Signature_Replay_Attacks": "Analyze the possible risks of Missing Protection against Signature Replay Attacks vulnerability in these codes: ",
    "Outdated_Compiler_Version": "Analyze the possible risks of Outdated Compiler Version vulnerability in these codes: ",
    "Shadowing_State_Variables": "Analyze the possible risks of Shadowing State Variables vulnerability in these codes: ",
    "Signature_Malleability": "Analyze the possible risks of Signature Malleability vulnerability in these codes: ",
    "State_Variable_Default_Visibility": "Analyze the possible risks of State Variable Default Visibility vulnerability in these codes: ",
    "Uninitialized_Storage_Pointer": "Analyze the possible risks of Uninitialized Storage Pointer vulnerability in these codes: ",
    "Unprotected_SELFDESTRUCT_Instruction": "Analyze the possible risks of Unprotected SELFDESTRUCT Instruction vulnerability in these codes: ",
    "Weak_Sources_of_Randomness_from_Chain_Attributes": "Analyze the possible risks of Weak Sources of Randomness from Chain Attributes vulnerability in these codes: ",
    "Write_to_Arbitrary_Storage_Location": "Analyze the possible risks of Write to Arbitrary Storage Location vulnerability in these codes: ",
    "TSE_Hard_Address": "Many developers statically embed specific address values directly into smart contracts. These addresses are frequently designated as deployment targets for new contract instances. However, hard-coding such addresses compromises code modularity and reusability, hinders adaptability across different deployment environments, and introduces potential security vulnerabilities—particularly in cases where address assumptions become invalid due to environmental changes or upgrades.Based on the above definition of vulnerabilities and technical characteristics, please conduct a static analysis of the following smart contract source code to determine whether it contains such security flaws.The source code is as follows:",
    "TSE_Overflow": "Solidity supports multiple integer types, each defined by a specific data width. For instance, the smallest unsigned integer type is uint8, which can represent values ranging from 0 to 255. However, Solidity does not automatically trigger exceptions in the event of integer overflows. In practice, developers often assign values within loop structures. If a variable is initialized with an inappropriate integer type only inside the loop, overflow issues may arise. In more severe scenarios, such vulnerabilities can lead to program crashes or unexpected behavior.Based on the above definition of vulnerabilities and technical characteristics, please conduct a static analysis of the following smart contract source code to determine whether it contains such security flaws.Only consider the internal part of the loop control statements.The source code is as follows:",
    "TSE_Suicide": "In smart contracts, ‘the absence of a contract termination method’ usually refers to the lack of a mechanism within the contract that can permanently halt the contract's functionality. This mechanism is often called an emergency stop (Emergency Stop) or a circuit breaker mechanism. Without this feature, when the contract detects a serious vulnerability or is subjected to an attack, the project owner is unable to stop the contract's deposit, withdrawal, or other critical operations, resulting in continuous loss of funds.Based on the above definition of vulnerabilities and technical characteristics, please conduct a static analysis of the following smart contract source code to determine whether it contains such security flaws.The source code is as follows:"
}

prompt_TSE_vulnerable_description = {
    "TSE_Hard_Address": "**Vulnerability Type Description:** Hardcoded address vulnerability. This occurs when developers embed specific Ethereum addresses directly into the contract code as literals, often used as targets for contract creation, privileged operations, or critical interactions. Hardcoding addresses severely reduces code flexibility and reusability, making the contract essentially a one-time deployment that cannot adapt to changing requirements or environments. More critically, it introduces significant security risks: if the hardcoded address becomes compromised, becomes obsolete, or was maliciously chosen during deployment, there is no mechanism to update or replace it without deploying an entirely new contract. This lack of upgradeability can lead to permanent fund loss, irreversible reliance on malicious contracts, or inability to respond to discovered vulnerabilities in the referenced address.",
    "TSE_Overflow": "**Vulnerability Type Description:** Mismatched type assignment vulnerability. This occurs when developers assign values between different integer types without proper bounds checking, particularly when a larger-range value is assigned to a smaller-range type (e.g., assigning a `uint256` value to a `uint8` variable). Solidity does **not** automatically revert or throw exceptions when such assignments cause truncation or overflow; instead, it performs silent truncation of higher-order bits. This becomes especially dangerous in contexts like loop counters or state variables where the assigned value's range is influenced by external factors or user inputs, making the final range unpredictable. The consequences can range from incorrect loop execution (causing denial of service) to more severe logical errors where variables hold unexpected values, potentially breaking contract invariants and enabling exploitable conditions.",
    "TSE_Suicide": "**Vulnerability Type Description:** Missing contract termination mechanism vulnerability. This occurs when a contract lacks a self-destruct or pause function that allows the owner to halt the contract in response to an attack. Once a vulnerability is exploited on the blockchain, the contract cannot be modified or stopped externally, enabling attackers to continuously drain funds without interruption. Implementing a termination function (e.g., `selfdestruct`) provides a failsafe that, when triggered by the owner, immediately stops contract execution and minimizes financial losses. Without such a mechanism, any discovered vulnerability becomes permanently exploitable.",
    "TSE_Greedy": "Vulnerability Type Description: Greedy contract vulnerability. This occurs when a contract is designed to receive ether but lacks any mechanism to withdraw or transfer the accumulated funds out of the contract. As a result, all ether sent to the contract becomes permanently locked within the contract address, with no functions available for users or owners to retrieve them. This creates an irreversible fund lock-up scenario where the contract acts as a black hole, accepting ether indefinitely but never releasing it, effectively rendering the funds inaccessible and lost.",
    "TSE_Strict_Balance": "Vulnerability Type Description: Strict equality comparison on contract balance vulnerability. This occurs when developers use `this.balance == value` as a condition for critical logic execution. Since `this.balance` represents the current ether balance of the contract, it is an externally influenceable variable that anyone can alter by sending ether to the contract, either through normal transactions or forced sends via `selfdestruct`. Attackers can manipulate the contract's balance to meet the exact equality condition, triggering unintended code paths, bypassing access controls, or disrupting expected contract behavior. This vulnerability stems from treating a dynamic, user-influenced value as a reliable state variable for precise conditional checks.",
    "Uncheck_ll_calls": "Vulnerability Type Description: Unchecked low-level call return values vulnerability. In Solidity, certain low-level functions such as `call`, `callcode`, `delegatecall`, and `send` do not propagate exceptions to the calling context when they encounter an error. Instead of reverting the entire transaction, they return a boolean `false` value and allow subsequent code to continue executing. Developers who assume these calls will always succeed and fail to check the return values may inadvertently let the contract continue execution in an inconsistent or unexpected state. This can lead to critical failures where operations proceed despite external calls failing, potentially compromising the contract's logic and fund safety.",
    "Reentrancy": "Vulnerability Type Description: Reentrancy vulnerability. This occurs when the contract makes an external call (e.g., `address.call{value: ...}("")`) before updating its internal state variables (such as user balances). An attacker can exploit this by using a malicious contract's `fallback` or `receive` function triggered during the ETH transfer to re-enter the same function of the original contract. Since the contract's state has not been correctly updated yet, the withdrawal logic can be executed repeatedly, allowing the attacker to drain funds. The core issue is the **violation of the 'Checks-Effects-Interactions' pattern, which leaves the contract in an inconsistent state and unable to complete execution properly.",
    "Access_Control": "**Vulnerability Type Description:** Access Control Vulnerability. This occurs when a contract fails to properly restrict who can execute certain sensitive functions, such as withdrawing funds, minting tokens, or changing ownership. If critical functions are left unprotected (e.g., missing `onlyOwner` modifiers or improper permission checks), any external user can call them and gain unauthorized access to privileged operations or private data. The core issue is the **lack of proper authorization mechanisms, allowing attackers to exploit unprotected functions to take control of the contract, drain funds, or manipulate critical logic.**",
    "Integer_Overflow_and_Underflow": "Vulnerability Type Description: Arithmetic Overflow/Underflow. This occurs when a contract performs math operations on integers that go beyond the data type's limits (e.g., a uint8 exceeding 255 and resetting to 0). In older Solidity versions, this allowed attackers to manipulate balances or logic by forcing numbers to wrap around unexpectedly. The core issue is the lack of proper validation or safe math libraries, enabling attackers to alter numerical values and cause financial losses or contract failure.",
    "Transaction_Order_Dependence": "Vulnerability Type Description: Transaction Order Dependence (TOD) vulnerability, also known as front-running. This occurs when a contract's logic depends on the order of transactions, allowing attackers to observe pending transactions and front-run them with their own. By monitoring the mempool, attackers can submit competing transactions with higher gas prices to be executed first, exploiting predictable state changes for profit."
}

prompt_TSE_vulnerable_fix_template = {
    "Reentrancy": {
        "fixTemplates": [
            {
                "id": "FT-1.1",
                "name": "Replace message call with send/transfer",
                "vulnerablePattern": "address.call.value(ethers)()",
                "securePattern": "address.transfer(ethers) or address.send(ethers)",
                "description": "Replace low-level .call.value() with .transfer() or .send() to limit gas to 2300 and prevent reentrancy attacks"
            },
            {
                "id": "FT-1.2",
                "name": "Move state changes before external calls",
                "vulnerablePattern": "External call first, then state updates",
                "securePattern": "State updates first, then external calls",
                "description": "Apply Checks-Effects-Interactions pattern by moving all state changes before any external calls to prevent reentrancy"
            }
        ]
    },
    "Uncheck_ll_calls": {
        "fixTemplates": [
            {
                "id": "FT-2.1",
                "name": "Check return value of external call",
                "vulnerablePattern": "address.transfer(value);",
                "securePattern": "bool success = address.transfer(value); require(success);",
                "description": "Add require() check to verify the return value of transfer(). If the external call fails, the transaction will revert automatically, preventing unhandled failures and inconsistent contract state."
            },
            {
                "id": "FT-2.3",
                "name": "Add return value check",
                "vulnerablePattern": "address.external_calls(ethers);",
                "securePattern": "if(!address.external_calls(ethers)) { throw; } or require(address.external_calls(ethers));",
                "description": "Check the return value of low-level external calls. Unlike high-level functions that revert on failure, low-level calls return false without throwing an exception, allowing the contract to continue execution in an inconsistent state."
            },
            {
                "id": "FT-2.2",
                "name": "Replace external call function",
                "vulnerablePattern": "address.external_calls(ethers);",
                "securePattern": "address.transfer(ethers);",
                "description": "Replace low-level external calls with transfer() which automatically reverts on failure and limits gas to 2300, preventing both unhandled failures and reentrancy attacks."
            }

        ]
    },
    "TSE_Greedy": {
        "fixTemplates": [
            {
                "id": "FT-5",
                "name": "Implement self-destruct function for fund recovery",
                "vulnerablePattern": "Contract lacks any mechanism to withdraw or recover funds",
                "securePattern": "function kill() public onlyOwner { selfdestruct(owner); }",
                "description": "Add a self-destruct function protected by proper access control that allows the contract owner to terminate the contract and transfer all remaining funds to a designated address. This provides an emergency stop mechanism in case of vulnerability discovery or contract migration needs."
            }
        ]
    },
    "TSE_Strict_Balance": {
        "fixTemplates": [
            {
                "id": "FT-6",
                "name": "Use balance range check instead of strict equality",
                "vulnerablePattern": "require(this.balance == value);",
                "securePattern": "require(this.balance >= value && this.balance < value + delta);",
                "description": "Replace strict equality checks on contract balance with range-based checks. Contract balance (this.balance) is an externally influenceable variable that anyone can alter by sending ether through normal transactions or forced sends via selfdestruct. Using a range check prevents attackers from manipulating the balance to meet exact equality conditions and bypass contract logic."
            }
        ]
    },
    "TSE_Suicide": {
        "fixTemplates": [
            {
                "id": "FT-9",
                "name": "Add contract termination mechanism",
                "vulnerablePattern": "Contract lacks any emergency stop or self-destruct function",
                "securePattern": "function terminate() public onlyOwner { require(this.balance == 0); selfdestruct(owner); }",
                "description": "Implement a termination function (selfdestruct) protected by access control that allows the contract owner to kill the contract when a vulnerability is discovered. Once a contract is deployed on the blockchain, it cannot be modified or stopped externally. Without a termination mechanism, attackers can continuously exploit any discovered vulnerability and drain funds repeatedly. Adding a self-destruct function provides an emergency failsafe that immediately stops contract execution and transfers remaining funds to a safe address, minimizing financial losses."
            }
        ]
    },
    "TSE_Overflow": {
        "fixTemplates": [
            {
                "id": "FT-7",
                "name": "Use maximum-range data types by default",
                "vulnerablePattern": "for(uint8 i = 0; i < val; i++)",
                "securePattern": "for(uint256 i = 0; i < val; i++) or for(uint i = 0; i < val; i++)",
                "description": "Always use uint256 (or its alias uint) for loop counters and general-purpose integer variables instead of smaller types like uint8, uint16, or uint32. Smaller types can overflow unexpectedly if the loop counter exceeds their maximum value, leading to infinite loops or denial of service. uint256 provides the maximum range (0 to 2^256-1) and is gas-optimized by the EVM."
            }
        ]
    },
    "TSE_Hard_Address": {
        "fixTemplates": [
            {
                "id": "FT-8",
                "name": "Use function parameters to initialize address variables",
                "vulnerablePattern": "function method() { ...0xeeeeeee...; }",
                "securePattern": "function method(address param0) { ...param0...; }",
                "description": "Replace hardcoded address literals within function bodies with function parameters. Hardcoding addresses reduces contract flexibility, makes contracts non-upgradable, and introduces security risks if the hardcoded address becomes compromised or obsolete. Passing addresses as parameters allows the same contract logic to be reused with different addresses and enables better testing and deployment flexibility."
            }
        ]
    },
    "Integer_Overflow_and_Underflow": {
        "fixTemplates": [
            {
                "id": "FT-3.1",
                "name": "Validate Arithmetic Operation Results",
                "vulnerablePattern": "a = b + c;",
                "securePattern": "// Addition\na += b;\nrequire(a >= b || a >= c);>= b);",
                "description": "Add necessary validation checks before performing arithmetic operations to prevent integer overflow/underflow. Addition operations must verify that the result is not less than either addend; compound assignment operators must follow the same validation principles. These validations are especially important in Solidity versions below 0.8.0 to effectively prevent fund loss and logic errors caused by arithmetic overflow."
            },
            {
                "id": "FT-3.2",
                "name": "Validate Arithmetic Operation Results",
                "vulnerablePattern": "a = b - c;",
                "securePattern": "// Subtraction\nrequire(b >= c);\na = b - c; ",
                "description": "Add necessary validation checks before performing arithmetic operations to prevent integer overflow/underflow. subtraction operations must verify that the minuend is not less than the subtrahend; compound assignment operators must follow the same validation principles. These validations are especially important in Solidity versions below 0.8.0 to effectively prevent fund loss and logic errors caused by arithmetic overflow."
            },
            {
                "id": "FT-3.3",
                "name": "Validate Arithmetic Operation Results",
                "vulnerablePattern": "a = b * c;",
                "securePattern": "// Multiplication\na = b * c;\nrequire(c == a / b);",
                "description": "Add necessary validation checks before performing arithmetic operations to prevent integer overflow/underflow. multiplication operations must verify the correctness of division results; compound assignment operators must follow the same validation principles. These validations are especially important in Solidity versions below 0.8.0 to effectively prevent fund loss and logic errors caused by arithmetic overflow."
            },
            {
                "id": "FT-3.4",
                "name": "Validate Arithmetic Operation Results",
                "vulnerablePattern": "a += b;",
                "securePattern": "// Addition assignment\na += b;\nrequire(a >= b);",
                "description": "Add necessary validation checks before performing arithmetic operations to prevent integer overflow/underflow. Addition operations must verify that the result is not less than either addend; compound assignment operators must follow the same validation principles. These validations are especially important in Solidity versions below 0.8.0 to effectively prevent fund loss and logic errors caused by arithmetic overflow."
            },
            {
                "id": "FT-3.5",
                "name": "Validate Arithmetic Operation Results",
                "vulnerablePattern": "a -= b;",
                "securePattern": "Subtraction assignment\nrequire(a >= b);\na -= b;",
                "description": "Add necessary validation checks before performing arithmetic operations to prevent integer overflow/underflow. subtraction operations must verify that the minuend is not less than the subtrahend;compound assignment operators must follow the same validation principles. These validations are especially important in Solidity versions below 0.8.0 to effectively prevent fund loss and logic errors caused by arithmetic overflow."
            },
            {
                "id": "FT-3.6",
                "name": "Validate Arithmetic Operation Results",
                "vulnerablePattern": "a *= b;",
                "securePattern": "// Multiplication assignment\nuint tmp = a;\n a *= b; \nrequire(b == a / tmp);",
                "description": "Add necessary validation checks before performing arithmetic operations to prevent integer overflow/underflow. multiplication operations must verify the correctness of division results; compound assignment operators must follow the same validation principles. These validations are especially important in Solidity versions below 0.8.0 to effectively prevent fund loss and logic errors caused by arithmetic overflow."
            }
        ]
    },
    "Access_Control": {
        "fixTemplates": [
            {
                "id": "FT-4.1",
                "name": "Replace tx.origin with msg.sender for Authentication",
                "vulnerablePattern": "tx.origin == owner",
                "securePattern": "msg.sender == owner",
                "description": "Replace tx.origin with msg.sender for identity verification. Using tx.origin for authentication is dangerous as it can lead to phishing attacks where a malicious contract calls your contract, making tx.origin refer to the original external account while the actual caller (msg.sender) is the malicious contract. This can trick the contract into executing privileged operations on behalf of an unwitting user."
            },
            {
                "id": "FT-4.2",
                "name": "Fix Incorrect Constructor Names",
                "vulnerablePattern": "function ContractName() { ... }  // Function with same name as contract (pre-Solidity 0.4.22)",
                "securePattern": "constructor() { ... }",
                "description": "Replace functions that share the same name as the contract with the proper constructor keyword. In older Solidity versions, constructors were defined as functions matching the contract name, which could accidentally become regular, callable functions if the contract name was changed or if there were typos. This could allow any user to call what was intended to be a one-time initialization function, potentially taking ownership or modifying critical contract parameters."
            },
            {
                "id": "FT-4.3",
                "name": "Add Missing Access Control Statements",
                "vulnerablePattern": "function sensitiveAction() { ... }  // No access control",
                "securePattern": "function sensitiveAction() { \n    require(msg.sender == contractOwner);\n    // Authority-sensitive statements\n}",
                "description": "Add explicit access control checks before executing sensitive operations. Without proper access modifiers like onlyOwner or explicit require statements, any user can call functions that should be restricted to administrators or specific roles. Always validate that the caller has the necessary permissions before allowing state changes, fund withdrawals, or privileged operations."
            }
        ]
    },
    "Transaction_Order_Dependence": {
        "fixTemplates": [
            {
                "id": "FT-5.1",
                "name": "Use Block Height for Time Restrictions",
                "vulnerablePattern": "function redeem() { require(now <= endTime); redeemTokens(); }",
                "securePattern": "function redeem() { require(block.number <= endBlock); redeemTokens(); }",
                "description": "Replace timestamp-based time restrictions with block height to ensure immutable and manipulation-resistant execution."
            },
            {
                "id": "FT-5.2",
                "name": "Commit-Reveal Scheme",
                "vulnerablePattern": "function bid() payable { highestBidder = msg.sender; highestBid = msg.value; }",
                "securePattern": "function commit(bytes32 hash) { commits[msg.sender] = hash; }\nfunction reveal(uint value, uint nonce) { require(keccak256(value, nonce) == commits[msg.sender]); processBid(value); }",
                "description": "Use commit-reveal pattern to hide actual values until after commitment phase."
            },
            {
                "id": "FT-5.3",
                "name": "Use Submarine Sends",
                "vulnerablePattern": "function claimPrize() { if(block.number <= deadline) pay(msg.sender); }",
                "securePattern": "function claimPrize(uint nonce) { bytes32 secret = keccak256(nonce, msg.sender); require(!used[secret]); used[secret]=true; processClaim(); }",
                "description": "Hide transaction details using secrets revealed in subsequent transactions."
            },
            {
                "id": "FT-5.4",
                "name": "Set Transaction Deadlines",
                "vulnerablePattern": "function swap(uint amount) { executeSwap(msg.sender, amount); }",
                "securePattern": "function swap(uint amount, uint deadline) { require(block.timestamp <= deadline); executeSwap(msg.sender, amount); }",
                "description": "Add deadlines to limit front-running window and ensure transaction validity."
            }

        ]
    }

}

prompt_vulnerable_type_ast = {
    "Authorization_through_tx.origin": "Analyze the AST data of the following Solidity contract to identify potential Authorization through tx.origin vulnerability risks:",
    "Delegatecall_to_Untrusted_Callee": "Analyze the AST data of the following Solidity contract to identify potential Delegatecall to Untrusted Callee vulnerability risks: ",
    "Integer_Overflow_and_Underflow": "Analyze the AST data of the following Solidity contract to identify potential Integer Overflow and Underflow vulnerability risks: (Please ignore the impact of solidity compiler versions 0.8.0 and above on the source code): ",
    "Presence_of_unused_variables": "Analyze the AST data of the following Solidity contract to identify potential Presence of unused variables vulnerability risks: ",
    "Reentrancy": "Analyze the AST data of the following Solidity contract to identify potential reentricity vulnerability risks: ",
    "Transaction_Order_Dependence": "Analyze the AST data of the following Solidity contract to identify potential Transaction Order Dependence vulnerability risks: ",
    "Unchecked_Call_Return_Value": "Analyze the AST data of the following Solidity contract to identify potential Unchecked Call Return Value vulnerability risks: ",
    "Unprotected_Ether_Withdrawal": "Analyze the AST data of the following Solidity contract to identify potential Unprotected Ether Withdrawal vulnerability risks: ",
    "Assert_Violation": "Analyze the AST data of the following Solidity contract to identify potential Assert Violation vulnerability risks: ",
    "Block_values_as_a_proxy_for_time": "Analyze the AST data of the following Solidity contract to identify potential Block values as a proxy for time vulnerability risks: ",
    "Code_With_No_Effects": "It is well known that 'SWC-135 Code With No Effects' includes problems like unused variables, pointless assignments to local variables, ineffective state variable updates, unreachable code, and mistakenly using the assignment operator = when the comparison operator == was intended.Analyze the AST data of the following Solidity contract to identify potential SWC-135-Code With No Effects vulnerability risks: ",
    "DoS_with_Failed_Call": "Analyze the AST data of the following Solidity contract to identify potential DoS with Failed Call vulnerability risks: ",
    "DoS_With_Block_Gas_Limit": "Analyze the AST data of the following Solidity contract to identify potential DoS With Block Gas Limit vulnerability risks: ",
    "Floating_Pragma": "Analyze the AST data of the following Solidity contract to identify potential Floating Pragma vulnerability risks: ",
    "Function_Default_Visibility": "Analyze the AST data of the following Solidity contract to identify potential Function Default Visibility vulnerability risks: ",
    "Hash_Collisions_With_Multiple_Variable_Length_Arguments": "Analyze the AST data of the following Solidity contract to identify potential Hash Collisions With Multiple Variable Length Arguments vulnerability risks: ",
    "Incorrect_Inheritance_Order": "Analyze the AST data of the following Solidity contract to identify potential Incorrect Inheritance Order vulnerability risks: ",
    "Insufficient_Gas_Griefing": "Analyze the AST data of the following Solidity contract to identify potential Insufficient Gas Griefing vulnerability risks: ",
    "Lack_of_Proper_Signature_Verification": "Analyze the AST data of the following Solidity contract to identify potential Lack of Proper Signature Verification vulnerability risks: ",
    "Missing_Protection_against_Signature_Replay_Attacks": "Analyze the AST data of the following Solidity contract to identify potential Missing Protection against Signature Replay Attacks vulnerability risks: ",
    "Outdated_Compiler_Version": "Analyze the AST data of the following Solidity contract to identify potential Outdated Compiler Version vulnerability risks: ",
    "Shadowing_State_Variables": "Analyze the AST data of the following Solidity contract to identify potential Shadowing State Variables vulnerability risks: ",
    "Signature_Malleability": "Analyze the AST data of the following Solidity contract to identify potential Signature Malleability vulnerability risks: ",
    "State_Variable_Default_Visibility": "Analyze the AST data of the following Solidity contract to identify potential State Variable Default Visibility vulnerability risks: ",
    "Uninitialized_Storage_Pointer": "Analyze the AST data of the following Solidity contract to identify potential Uninitialized Storage Pointer vulnerability risks: ",
    "Unprotected_SELFDESTRUCT_Instruction": "Analyze the AST data of the following Solidity contract to identify potential Unprotected SELFDESTRUCT Instruction vulnerability risks: ",
    "Weak_Sources_of_Randomness_from_Chain_Attributes": "Analyze the AST data of the following Solidity contract to identify potential Weak Sources of Randomness from Chain Attributes vulnerability risks: ",
    "Write_to_Arbitrary_Storage_Location": "Analyze the AST data of the following Solidity contract to identify potential Write to Arbitrary Storage Location vulnerability risks: "
}

prompt_vulnerable_type_ast_source_code = {
    "Authorization_through_tx.origin": "Analyze the code provided above to identify the potential Authorization through tx.origin vulnerability risk:",
    "Delegatecall_to_Untrusted_Callee": "Analyze the AST data of the following Solidity contract to identify potential Delegatecall to Untrusted Callee vulnerability risks: ",
    "Integer_Overflow_and_Underflow": "Analyze the AST data of the following Solidity contract to identify potential Integer Overflow and Underflow vulnerability risks: (Please ignore the impact of solidity compiler versions 0.8.0 and above on the source code): ",
    "Presence_of_unused_variables": "Analyze the AST data of the following Solidity contract to identify potential Presence of unused variables vulnerability risks: ",
    "Reentrancy": "Analyze the AST data of the following Solidity contract to identify potential reentricity vulnerability risks: ",
    "Transaction_Order_Dependence": "Analyze the AST data of the following Solidity contract to identify potential Transaction Order Dependence vulnerability risks: ",
    "Unchecked_Call_Return_Value": "Analyze the AST data of the following Solidity contract to identify potential Unchecked Call Return Value vulnerability risks: ",
    "Unprotected_Ether_Withdrawal": "Analyze the AST data of the following Solidity contract to identify potential Unprotected Ether Withdrawal vulnerability risks: ",
    "Assert_Violation": "Analyze the AST data of the following Solidity contract to identify potential Assert Violation vulnerability risks: ",
    "Block_values_as_a_proxy_for_time": "Analyze the AST data of the following Solidity contract to identify potential Block values as a proxy for time vulnerability risks: ",
    "Code_With_No_Effects": "It is well known that 'SWC-135 Code With No Effects' includes problems like unused variables, pointless assignments to local variables, ineffective state variable updates, unreachable code, and mistakenly using the assignment operator = when the comparison operator == was intended.Analyze the AST data of the following Solidity contract to identify potential SWC-135-Code With No Effects vulnerability risks: ",
    "DoS_with_Failed_Call": "Analyze the AST data of the following Solidity contract to identify potential DoS with Failed Call vulnerability risks: ",
    "DoS_With_Block_Gas_Limit": "Analyze the AST data of the following Solidity contract to identify potential DoS With Block Gas Limit vulnerability risks: ",
    "Floating_Pragma": "Analyze the AST data of the following Solidity contract to identify potential Floating Pragma vulnerability risks: ",
    "Function_Default_Visibility": "Analyze the AST data of the following Solidity contract to identify potential Function Default Visibility vulnerability risks: ",
    "Hash_Collisions_With_Multiple_Variable_Length_Arguments": "Analyze the AST data of the following Solidity contract to identify potential Hash Collisions With Multiple Variable Length Arguments vulnerability risks: ",
    "Incorrect_Inheritance_Order": "Analyze the AST data of the following Solidity contract to identify potential Incorrect Inheritance Order vulnerability risks: ",
    "Insufficient_Gas_Griefing": "Analyze the AST data of the following Solidity contract to identify potential Insufficient Gas Griefing vulnerability risks: ",
    "Lack_of_Proper_Signature_Verification": "Analyze the AST data of the following Solidity contract to identify potential Lack of Proper Signature Verification vulnerability risks: ",
    "Missing_Protection_against_Signature_Replay_Attacks": "Analyze the AST data of the following Solidity contract to identify potential Missing Protection against Signature Replay Attacks vulnerability risks: ",
    "Outdated_Compiler_Version": "Analyze the AST data of the following Solidity contract to identify potential Outdated Compiler Version vulnerability risks: ",
    "Shadowing_State_Variables": "Analyze the AST data of the following Solidity contract to identify potential Shadowing State Variables vulnerability risks: ",
    "Signature_Malleability": "Analyze the AST data of the following Solidity contract to identify potential Signature Malleability vulnerability risks: ",
    "State_Variable_Default_Visibility": "Analyze the AST data of the following Solidity contract to identify potential State Variable Default Visibility vulnerability risks: ",
    "Uninitialized_Storage_Pointer": "Analyze the AST data of the following Solidity contract to identify potential Uninitialized Storage Pointer vulnerability risks: ",
    "Unprotected_SELFDESTRUCT_Instruction": "Analyze the AST data of the following Solidity contract to identify potential Unprotected SELFDESTRUCT Instruction vulnerability risks: ",
    "Weak_Sources_of_Randomness_from_Chain_Attributes": "Analyze the AST data of the following Solidity contract to identify potential Weak Sources of Randomness from Chain Attributes vulnerability risks: ",
    "Write_to_Arbitrary_Storage_Location": "Analyze the AST data of the following Solidity contract to identify potential Write to Arbitrary Storage Location vulnerability risks: "
}

prompt_answer = '\nGiven the following smart contract code, answer the questions below ' \
                'and organize the result in a json format like {"result":"Yes","analyze":"...","vulnerable_code_info":[{"function":"...","vulnerable_code":"..."}]}' \
                'or {"result":"no",analyze:"nothing","vulnerable_code_info":[]} '

prompt_answer_ast = '\nGiven the AST of a compiled smart contract, answer the questions below ' \
                    'and organize the result in a json format like {"result":"Yes","analyze":"...","vulnerabilities":[{"location":{"code":["a+b","B+C"...],"function":"withdraw"}},{"location":{"code":["balance[msg.sender] = newBalance","uint256 newBalance = balance[msg.sender] + amount",...],"function":"deposit"}}...]}' \
                    'or {"result":"no",analyze:"nothing","vulnerabilities":[]} '

prompt_answer_ast_source_code = 'answer the questions below ' \
                                'and organize the result in a json format like {"result":"Yes","analyze":"...","vulnerabilities":[{"location":{"code":["...","...",...],"function":"..."}},....]}' \
                                'or {"result":"no",analyze:"nothing","vulnerabilities":[]} '

prompt_answer_fix = '''Task: Fix the identified vulnerability based on the provided materials. Task: Fix the identified vulnerability based on the provided materials.And do not repeat or quote the content of the user's question.You must only return the output in JSON format, and do not include any other content.The JSON must follow this exact format:{"fixedCodeSnippet": "...","remediationSummary": "..."} - fixedCodeSnippet: The complete fixed code snippet that addresses the vulnerability - remediationSummary: A brief explanation of what vulnerability was fixed and how'''

prompt_answer_vulnerable_type = {
    "Authorization_through_tx.origin": """\nGPT:{"result":"yes","analyze":"In the sendTo function, tx.origin is used to verify that the caller is the contract owner. tx.origin is a global variable that returns the initiator address of the entire transaction chain. The attacker can use this to invoke the sendTo function from an intermediate contract, which, since the tx.origin of the intermediate contract is still the attacker's external account address, is able to bypass authentication and perform unauthorized transfers.","vulnerable_code":["require(tx.origin == owner)"]}""",
    "Delegatecall_to_Untrusted_Callee": """\nGPT:{"result":"yes","analyze":"In the forward function, the passed callee contract function is called using delegatecall without any restrictions or validation. The external user can pass an arbitrary address by calling the forward function, which allows the attacker to pass a malicious contract address. As a result, the code of the malicious contract is executed in the context of the current contract, which may cause the state of the contract to be maliciously modified, such as modifying the owner variable to seize control of the contract.","vulnerable_code":["require(callee.delegatecall(_data));"]}""",
    "Integer_Overflow_and_Underflow": """\nGPT:{"result":"yes","analyze":"In the deposit function, an arithmetic overflow occurs when the value of balance plus amount exceeds the maximum value that can be represented by the uint256 type. In the withdraw function, although there is a require(amount <= balance) check, if the balance becomes 0 due to a previous addition overflow and a malicious caller tries to withdraw an amount greater than 0, In Solidity versions prior to 0.8.0, this subtraction will cause an underflow and balance will become a very large number.","vulnerable_code":[ "balance = balance + amount;","balance = balance - amount;"]}""",
    "Presence_of_unused_variables": """\nGPT:{"result":"yes","analyze":"In the DerivedA contract, the variable i is defined as A i = A(1); but it is not used anywhere within the functions of the DerivedA contract. ","vulnerable_code":["A i = A(1);"]}""",
    "Reentrancy": """\nGPT:{"result":"yes","analyze":"This type of vulnerability occurs when a contract allows an external call to another untrusted contract before it resolves its own state changes. In this case, the function makes an external call to `msg.sender.call{value: _amount}("")` before updating the user's balance with `balances[msg.sender] -= amount;The critical issue here is that the external call to `msg.sender` is made before the balance is updated. If `msg.sender` is a contract with a fallback or receive function, it could potentially call back into the `withdraw` function before the balance is updated, allowing it to withdraw more funds than it should be able to.","vulnerable_code":[ "(bool success, ) = msg.sender.call{value: _amount}("")"]""",
    "Transaction_Order_Dependence": """\nGPT:{"result":"yes","analyze":"The contract has a transaction order dependency vulnerability. In the setReward function, it first transfers the existing reward to the owner and then updates reward with the new msg.value. If an attacker can call the claimReward function immediately after the setReward function is called but before the reward is updated, they can claim the old reward value. Also, the claimReward function does not have proper access control, allowing any user to call it if the conditions are met.","vulnerable_code":["function setReward() public payable {", "function claimReward(uint256 submission) {"]}""",
    "Unchecked_Call_Return_Value": """\nGPT:{"result":"yes","analyze":"The transferFunds function tries to send a specified amount of ether to the beneficiary address. However, it uses call for external invocation and does not check the return value of call. If the beneficiary is a contract address and the contract's fallback or receive function fails, the call call will return false, but the contract doesn't check this return value. The execution will still proceed and the TransferSuccessful event will fire, giving the caller the false impression that the contract execution was successful.","vulnerable_code":[ "beneficiary.call{value: amountToTransfer}("");"]}""",
    "Unprotected_Ether_Withdrawal": """\nGPT:{"result":"yes","analyze":"In the TokenSaleChallenge contract, the sell function sends Ether to msg.sender without fully verifying the caller's authority. Although there is a check on the balance, there is no proper access control for the withdrawal operation, which may allow unauthorized users to withdraw Ether from the contract, presenting an "Unprotected Ether Withdrawal" vulnerability.","vulnerable_code":[ "function sell(uint256 numTokens) public {"]}"""
}
