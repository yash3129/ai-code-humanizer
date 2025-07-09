const esprima = require("esprima");
const escodegen = require("escodegen");
const fs = require("fs");

const renameMap = {
    temp: "result",
    x: "total",
    y: "count",
    z: "index",
    a: "valueA",
    b: "valueB"
};

function humanizeJS(code) {
    let ast = esprima.parseScript(code, { comment: true, loc: true, range: true, tokens: true });

    const comments = [];

    function renameIdentifiers(node) {
        if (Array.isArray(node)) {
            node.forEach(renameIdentifiers);
        } else if (node && typeof node === "object") {
            if (node.type === "Identifier" && renameMap[node.name]) {
                const old = node.name;
                const renamed = renameMap[old];
                node.name = renamed;

                if (!node._commented) {
                    comments.push({
                        type: "Line",
                        value: ` Renamed '${old}' to '${renamed}'`,
                        range: node.range,
                    });
                    node._commented = true;
                }
            }

            if (node.type === "FunctionDeclaration") {
                const funcName = node.id ? node.id.name : "unknown";
                comments.push({
                    type: "Line",
                    value: ` Function: ${funcName}\n Description: TODO - Describe this function`,
                    range: node.range,
                });
            }

            if (node.type === "ReturnStatement") {
                comments.push({
                    type: "Line",
                    value: " Return final result",
                    range: node.range,
                });
            }

            for (let key in node) {
                if (node[key] && typeof node[key] === "object") {
                    renameIdentifiers(node[key]);
                }
            }
        }
    }

    renameIdentifiers(ast);

    ast.comments = comments;

    return escodegen.generate(ast, {
        comment: true,
        format: {
            indent: {
                style: "  "
            }
        }
    });
}

if (require.main === module) {
    const inputFile = process.argv[2];
    const inputCode = fs.readFileSync(inputFile, "utf-8");
    const output = humanizeJS(inputCode);
    console.log(output);
}

module.exports = { humanizeJS };