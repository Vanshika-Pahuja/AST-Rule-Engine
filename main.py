
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker
import json
import logging

app = Flask(__name__)
Base = declarative_base()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Rule(Base):
    __tablename__ = 'rules'
    id = Column(Integer, primary_key=True)
    rule_string = Column(String, nullable=False)
    ast = Column(Text, nullable=False)

engine = create_engine('sqlite:///rules.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

class Node:
    def __init__(self, type, value, left=None, right=None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right

    def to_dict(self):
        return {
            'type': self.type,
            'value': self.value,
            'left': self.left.to_dict() if self.left else None,
            'right': self.right.to_dict() if self.right else None
        }

    @classmethod
    def from_dict(cls, data):
        if data is None:
            return None
        return cls(
            type=data['type'],
            value=data['value'],
            left=cls.from_dict(data['left']),
            right=cls.from_dict(data['right'])
        )

def parse_rule_string(rule_string):
    tokens = rule_string.replace('(', ' ( ').replace(')', ' ) ').split()

    def parse_expression():
        stack = [[]]
        for token in tokens:
            if token == '(':
                stack.append([])
            elif token == ')':
                expr = stack.pop()
                stack[-1].append(expr)
            elif token in ['AND', 'OR']:
                stack[-1].append(token)
            else:
                stack[-1].append(token)
        
        def build_tree(expr):
            if isinstance(expr, list):
                if len(expr) == 1:
                    return build_tree(expr[0])
                elif 'OR' in expr:
                    idx = expr.index('OR')
                    return Node('operator', 'OR', build_tree(expr[:idx]), build_tree(expr[idx+1:]))
                elif 'AND' in expr:
                    idx = expr.index('AND')
                    return Node('operator', 'AND', build_tree(expr[:idx]), build_tree(expr[idx+1:]))
            return Node('operand', ' '.join(expr))
        
        return build_tree(stack[0])
    
    return parse_expression()

def evaluate_ast(ast, data):
    if ast.type == 'operator':
        if ast.value == 'AND':
            return evaluate_ast(ast.left, data) and evaluate_ast(ast.right, data)
        elif ast.value == 'OR':
            return evaluate_ast(ast.left, data) or evaluate_ast(ast.right, data)
    elif ast.type == 'operand':
        left, op, right = ast.value.split()
        left_value = data.get(left)
        right_value = int(right) if right.isdigit() else right.strip("'")
        if op == '>':
            return left_value > right_value
        elif op == '<':
            return left_value < right_value
        elif op == '=':
            return left_value == right_value
    return False

@app.route('/create_rule', methods=['POST'])
def create_rule():
    rule_string = request.json['rule_string']
    ast = parse_rule_string(rule_string)
    rule = Rule(rule_string=rule_string, ast=json.dumps(ast.to_dict()))
    session.add(rule)
    session.commit()
    return jsonify({'id': rule.id, 'ast': rule.ast})

@app.route('/combine_rules', methods=['POST'])
def combine_rules():
    rule_ids = request.json['rule_ids']
    rules = session.query(Rule).filter(Rule.id.in_(rule_ids)).all()
    combined_ast = Node('operator', 'AND', *[Node.from_dict(json.loads(rule.ast)) for rule in rules])
    combined_rule_string = " AND ".join([rule.rule_string for rule in rules])
    combined_rule = Rule(rule_string=combined_rule_string, ast=json.dumps(combined_ast.to_dict()))
    session.add(combined_rule)
    session.commit()
    return jsonify({'id': combined_rule.id, 'combined_ast': json.dumps(combined_ast.to_dict())})

@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule():
    rule_id = request.json['rule_id']
    rule = session.query(Rule).filter_by(id=rule_id).first()
    if not rule:
        return jsonify({'error': 'Rule not found'}), 404
    ast = Node.from_dict(json.loads(rule.ast))
    data = request.json['data']
    result = evaluate_ast(ast, data)
    return jsonify({'result': result})

@app.route('/modify_rule', methods=['POST'])
def modify_rule():
    try:
        rule_id = request.json['rule_id']
        new_rule_string = request.json['new_rule_string']
        rule = session.query(Rule).filter_by(id=rule_id).first()
        if rule:
            rule.rule_string = new_rule_string
            rule.ast = json.dumps(parse_rule_string(new_rule_string).to_dict())
            session.commit()
            return jsonify({'message': 'Rule updated successfully'})
        else:
            return jsonify({'message': 'Rule not found'}), 404
    except Exception as e:
        logging.error(f"Error modifying rule: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
