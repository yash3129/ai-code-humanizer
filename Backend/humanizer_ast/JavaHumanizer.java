import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.body.VariableDeclarator;
import com.github.javaparser.ast.expr.NameExpr;
import com.github.javaparser.ast.expr.SimpleName;
import com.github.javaparser.ast.stmt.ForStmt;
import com.github.javaparser.ast.stmt.IfStmt;
import com.github.javaparser.ast.visitor.ModifierVisitor;
import com.github.javaparser.ast.visitor.Visitable;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class JavaHumanizer {
    public static void main(String[] args) throws IOException {
        File inputFile = new File("Test.java");
        CompilationUnit cu = StaticJavaParser.parse(inputFile);

        Map<String, String> replacements = new HashMap<>();
        replacements.put("temp", "result");
        replacements.put("a", "valueA");
        replacements.put("b", "valueB");
        replacements.put("x", "totalSum");
        replacements.put("y", "countVal");
        replacements.put("z", "loopIndex");
        replacements.put("i", "index");

        cu.accept(new ModifierVisitor<Void>() {
            @Override
            public Visitable visit(MethodDeclaration md, Void arg) {
                if (!md.getJavadocComment().isPresent()) {
                    String doc = "/**\n * " + md.getNameAsString() + " method\n * Parameters: " + md.getParameters() + "\n */";
                    md.setJavadocComment(doc);
                }
                return super.visit(md, arg);
            }
        }, null);

        cu.accept(new ModifierVisitor<Void>() {
            @Override
            public Visitable visit(VariableDeclarator vd, Void arg) {
                String oldName = vd.getNameAsString();
                if (replacements.containsKey(oldName)) {
                    vd.setName(replacements.get(oldName));
                }
                return super.visit(vd, arg);
            }

            @Override
            public Visitable visit(NameExpr ne, Void arg) {
                String name = ne.getNameAsString();
                if (replacements.containsKey(name)) {
                    ne.setName(replacements.get(name));
                }
                return super.visit(ne, arg);
            }
        }, null);

        // Add inline comments
        cu.findAll(VariableDeclarator.class).forEach(vd -> {
            vd.setLineComment("Variable assignment");
        });

        cu.findAll(IfStmt.class).forEach(stmt -> {
            stmt.setLineComment("Conditional check");
        });

        cu.findAll(ForStmt.class).forEach(stmt -> {
            stmt.setLineComment("Looping over items");
        });

        System.out.println(cu.toString());
        System.out.flush();
    }
}