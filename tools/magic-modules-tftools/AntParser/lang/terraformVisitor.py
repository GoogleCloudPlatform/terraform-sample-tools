# Generated from terraform.g4 by ANTLR 4.10.1
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .terraformParser import terraformParser
else:
    from terraformParser import terraformParser

# This class defines a complete generic visitor for a parse tree produced by terraformParser.


class terraformVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by terraformParser#file_.
    def visitFile_(self, ctx: terraformParser.File_Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by terraformParser#terraform.
    def visitTerraform(self, ctx: terraformParser.TerraformContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by terraformParser#resource.
    def visitResource(self, ctx: terraformParser.ResourceContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by terraformParser#data.
    def visitData(self, ctx: terraformParser.DataContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by terraformParser#provider.
    def visitProvider(self, ctx: terraformParser.ProviderContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by terraformParser#output.
    def visitOutput(self, ctx: terraformParser.OutputContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by terraformParser#local.
    def visitLocal(self, ctx: terraformParser.LocalContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by terraformParser#module.
    def visitModule(self, ctx: terraformParser.ModuleContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by terraformParser#variable.
    def visitVariable(self, ctx: terraformParser.VariableContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by terraformParser#block.
    def visitBlock(self, ctx: terraformParser.BlockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by terraformParser#blocktype.
    def visitBlocktype(self, ctx: terraformParser.BlocktypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by terraformParser#resourcetype.
    def visitResourcetype(self, ctx: terraformParser.ResourcetypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by terraformParser#name.
    def visitName(self, ctx: terraformParser.NameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by terraformParser#label.
    def visitLabel(self, ctx: terraformParser.LabelContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by terraformParser#blockbody.
    def visitBlockbody(self, ctx: terraformParser.BlockbodyContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by terraformParser#argument.
    def visitArgument(self, ctx: terraformParser.ArgumentContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by terraformParser#identifier.
    def visitIdentifier(self, ctx: terraformParser.IdentifierContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by terraformParser#identifierchain.
    def visitIdentifierchain(self, ctx: terraformParser.IdentifierchainContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by terraformParser#inline_index.
    def visitInline_index(self, ctx: terraformParser.Inline_indexContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by terraformParser#expression.
    def visitExpression(self, ctx: terraformParser.ExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by terraformParser#forloop.
    def visitForloop(self, ctx: terraformParser.ForloopContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by terraformParser#section.
    def visitSection(self, ctx: terraformParser.SectionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by terraformParser#val.
    def visitVal(self, ctx: terraformParser.ValContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by terraformParser#functioncall.
    def visitFunctioncall(self, ctx: terraformParser.FunctioncallContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by terraformParser#functionname.
    def visitFunctionname(self, ctx: terraformParser.FunctionnameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by terraformParser#functionarguments.
    def visitFunctionarguments(self, ctx: terraformParser.FunctionargumentsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by terraformParser#index.
    def visitIndex(self, ctx: terraformParser.IndexContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by terraformParser#filedecl.
    def visitFiledecl(self, ctx: terraformParser.FiledeclContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by terraformParser#list_.
    def visitList_(self, ctx: terraformParser.List_Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by terraformParser#map_.
    def visitMap_(self, ctx: terraformParser.Map_Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by terraformParser#string.
    def visitString(self, ctx: terraformParser.StringContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by terraformParser#signed_number.
    def visitSigned_number(self, ctx: terraformParser.Signed_numberContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by terraformParser#operator_.
    def visitOperator_(self, ctx: terraformParser.Operator_Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by terraformParser#number.
    def visitNumber(self, ctx: terraformParser.NumberContext):
        return self.visitChildren(ctx)


del terraformParser
