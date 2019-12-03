/*
이름 : 최재우
학번 : 2014041005
*/
#include <iostream>
#include <fstream>
#include <string>
#include <stdlib.h>

using namespace std;


struct node {
	char key[10];
	char value[10];
	node *left = NULL;
	node *right = NULL;
	node *p = NULL;
	char color[7];
};
struct tree {
	node *nil;
	node *root;
};
tree *Tree = (tree*)malloc(sizeof(tree));

void LeftRotate(tree *Tree, node *x);
void RightRotate(tree *Tree, node *x);
void RBInsertFixup(tree *Tr, node *z)
{
	node *y;
	//cout << z->color;
	while (strcmp(z->p->color, "red") == 0)
	{
		if (z->p == z->p->p->left)
		{
			y = z->p->p->right;
			if (strcmp(y->color, "red") == 0)
			{
				strcpy(z->p->color, "black");
				strcpy(y->color, "black");
				strcpy(z->p->p->color, "red");
				z = z->p->p;
			}
			else  
			{
				if (z == z->p->right)
				{
					z = z->p;
					LeftRotate(Tr, z);
				}
				strcpy(z->p->color, "black");
				strcpy(z->p->p- d>color, "red");
				RightRotate(Tr, z->p->p);
			}
			
		}
		else
		{
			y = z->p->p->left;
			if (strcmp(y->color, "red") == 0)
			{
				strcpy(z->p->color, "black");
				strcpy(y->color, "black");
				strcpy(z->p->p->color, "red");
				z = z->p->p;
			}
			else 
			{
				if (z == z->p->left)
				{
					z = z->p;
					RightRotate(Tr, z);
				}
				strcpy(z->p->color, "black");
				strcpy(z->p->p->color, "red");
				LeftRotate(Tr, z->p->p);
			}
			
		}
	}
	strcpy(Tr->root->color, "black");
}
void TreeRBInsert(tree *Tr, node *nd)
{
	
	node *y = Tr->nil;
	node *x = Tr->root;
	//cout << nd->color;
	while (x != Tr->nil)
	{
		y = x;
		if (atoi(nd->key) < atoi(x->key))
			x = x->left;
		else
			x = x->right;
	}
	nd->p = y;
	if (y == Tr->nil)
		Tr->root = nd;
	else if (atoi(y->key) > atoi(nd->key))
		y->left = nd;
	else
		y->right = nd;
	nd->left = Tree->nil;
	nd->right = Tree->nil;
	strcpy(nd->color, "red");
	RBInsertFixup(Tr, nd);
}
void InorderTreeWalk(tree *Tr,node *x)
{
	if (x != Tr->nil)
	{
		InorderTreeWalk(Tr,x->left);
		cout << "(" << x->key << " " << x->value << " "<< x->color << ")"<<endl;
		InorderTreeWalk(Tr,x->right);
	}
}
void PostorderTreeWalk(tree *Tr,node *x)
{
	if (x != Tr->nil)
	{
		PostorderTreeWalk(Tr,x->left);
		PostorderTreeWalk(Tr,x->right);
		cout << "(" << x->key << " " << x->value << " " << x->color<<")" << endl;
	}
}
void PreorderTreeWalk(tree *Tr,node *x)
{
	if (x != Tr->nil)
	{
		cout << "(" << x->key << " " << x->value << " " << x->color<<")" << endl;
		PreorderTreeWalk(Tr,x->left);
		PreorderTreeWalk(Tr,x->right);
	}
}
node* TreeSearch(tree *Tr,node* x, int k)
{
	if (x ==  Tr->nil || k == atoi(x->key))
		return x;
	if (k < atoi(x->key))
		return TreeSearch(Tr,x->left, k);
	else return TreeSearch(Tr,x->right, k);
}
node* TreeMinimum(tree *Tr,node* x)
{
	while (x->left != Tr->nil)
	{
		x = x->left;
	}
	return x;
}
node* TreeMaximum(tree *Tr,node* x)
{
	while (x->right != Tr->nil)
	{
		x = x->right;
	}
	return x;
}
node* TreeSuccessor(tree *Tr,node* x)
{
	node *y;
	if (x->right != Tr->nil)
		return TreeMinimum(Tr,x->right);
	y = x->p;
	while (y != Tr->nil && x == y->right)
	{
		x = y;
		y = y->p;
	}
	return y;
}
node* TreePredecessor(tree *Tr,node* x)
{
	node *y;
	if (x->left != Tr->nil)
		return TreeMaximum(Tr,x->left);
	y = x->p;
	while (y != Tr->nil && x == y->left)
	{
		x = y;
		y = y->p;
	}
	return y;
}
void Transplant(tree *Tree, node *u, node *v)
{
	if (u->p == Tree->nil)
		Tree->root = v;
	else if (u == u->p->left)
		u->p->left = v;
	else
		u->p->right = v;
	if (v != Tree->nil)
		v->p = u->p;
}
void RBDeleteFixup(tree *Tr, node *x)
{
	node *w;
	while (x != Tr->root && (strcmp(x->color, "black") == 0))
	{
		if (x == x->p->left)
		{
			w = x->p->left;
			if (strcmp(w->color, "red") == 0)
			{
				strcpy(w->color, "black");
				strcpy(x->p->color, "red");
				LeftRotate(Tr, x->p);
				w = x->p->right;
			}
			if (strcmp(w->left->color, "black") == 0 && strcmp(w ->right ->color, "black") == 0)
			{
				strcpy(w->color, "red");
				x = x->p;
			}
			else
			{
				if (strcmp(w->right->color, "black") == 0)
				{
					strcpy(w->left->color, "black");
					strcpy(w->color, "red");
					RightRotate(Tr, w);
					w = x->p->right;
				}
				strcpy(w->color, x->p->color);
				strcpy(x->p->color, "black");
				strcpy(w->right->color, "black");
				LeftRotate(Tr, x->p);
				x = Tr->root;
			}
		}
		else
		{
			w = x->p->right;
			if (strcmp(w->color, "red") == 0)
			{
				strcpy(w->color, "black");
				strcpy(x->p->color, "red");
				RightRotate(Tr, x->p);
				w = x->p->left;
			}
			if (strcmp(w->right->color, "black") == 0 && strcmp(w->left->color, "black") == 0)
			{
				strcpy(w->color, "red");
				x = x->p;
			}
			else
			{
				if (strcmp(w->left->color, "black") == 0)
				{
					strcpy(w->right->color, "black");
					strcpy(w->color, "red");
					LeftRotate(Tr, w);
					w = x->p->left;
				}
				strcpy(w->color, x->p->color);
				strcpy(x->p->color, "black");
				strcpy(w->left->color, "black");
				RightRotate(Tr, x->p);
				x = Tr->root;
			}
		}
	}
}
void TreeRBDelete(tree *Tree, node *z)
{
	char yoc[7];
	node *y, *x;
	y = z;
	strcpy(yoc, y->color);
	if (z->left == Tree->nil)
	{
		x = z->right;
		Transplant(Tree, z, z->right);
	}
	else if (z->right == Tree->nil)
	{
		x = z->left;
		Transplant(Tree, z, z->right);
	}
	else
	{
		y = TreeMinimum(Tree,z->right);
		strcpy(yoc, y->color);
		x = y->right;
		if (y->p == z)
		{
			x->p = y;
		}
		else
		{
			Transplant(Tree, y, y->right);
			y->right = z->right;
			y->right->p = y;
		}
		Transplant(Tree, z, y);
		y->left = z->left;
		y->left->p = y;
		strcpy(y->color, z->color);
	}
	if (strcmp(yoc, "black") == 0)
		RBDeleteFixup;
}
void LeftRotate(tree *Tree, node *x)
{
	node *y;
	y = x->right;
	x->right = y->left;
	if (y->left != Tree->nil)
	{
		y->left->p = x;
	}
	y->p = x->p;
	if (x->p == Tree->nil)
		Tree->root = y;
	else if (x == x->p->left)
		x->p->left = y;
	else
		x->p->right = y;
	y->left = x;
	x->p = y;
}
void RightRotate(tree *Tree, node *x)
{
	node *y;
	y = x->left;
	x->left = y->right;
	if (y->right != Tree->nil)
		y->right->p = x;
	y->p = x->p;
	if (x->p == Tree->nil)
		Tree->root = y;
	else if (x == x->p->right)
		x->p->right = y;
	else
		x->p->left = y;
	y->right = x;
	x->p = y;
}

void main()
{
	char tcolor[7];
	int dltKey;
	int scnode;
	node *temp;
	node *temp1;
	node *dlt;
	int num1, num2;
	int select;
	
	Tree->nil = (node*)malloc(sizeof(node));
	strcpy(Tree->nil->color, "black");
	ifstream input("input.txt");
	Tree->root = Tree->nil;
	//Tree->root->p = Tree->nil;
	
	while (1)
	{
		cout << "여기서부터";
		temp = Tree->root;
		/*while (temp != Tree->nil)
		{
			cout << temp->key<<endl;
			cout << temp->right->key<<endl;
			cout << temp->left->key << endl;
			temp = temp->left;
			
		}*/
		cout << "1. inoder walk" << endl;
		cout << "2. preorder walk" << endl;
		cout << "3. postorder walk" << endl;
		cout << "4. insert" << endl;
		cout << "5. delete" << endl;
		cout << "6. search" << endl;
		cout << "7. minimum" << endl;
		cout << "8. maximum" << endl;
		cout << "9. successor" << endl;
		cout << "10. predecessor" << endl;
		cout << "11. 종료" << endl;
		cout << "메뉴를 고르시오 : ";
		cin >> select;
		switch (select)
		{
		case 1:
		{
			system("cls");
			InorderTreeWalk(Tree,temp);
			break;
		}
		case 2:
		{
			system("cls");
			PreorderTreeWalk(Tree,temp);
			break;
		}
		case 3:
		{
			system("cls");
			PostorderTreeWalk(Tree,temp);
			break;
		}
		case 4:
		{
			system("cls");
			if (!input.eof())
			{
				temp1 = (node *)malloc(sizeof(node));
				input >> num1;
				input >> num2;
				itoa(num1, temp1->key, 10);
				itoa(num2, temp1->value, 10);
				//input >> tcolor;

				//strcpy(temp1->color, tcolor);
				temp1->p = NULL;
				temp1->right = NULL;
				temp1->left = NULL;
				
				TreeRBInsert(Tree, temp1);
				
			}
			else
				cout << "파일에 다음 데이터가 없습니다."<<endl;
			break;
		}
		case 5:
		{
			system("cls");
			cout << "삭제 하고 싶은 노드의 키값을 입력하시오 : "<<endl;
			cin >> dltKey;
			dlt = TreeSearch(Tree,temp, dltKey);
			if (dlt != Tree->nil)
				TreeRBDelete(Tree, dlt);
			else
				cout << "노드가 존재하지 않습니다."<<endl;
			break;
		}
		case 6:
		{
			node *sc;
			cout << "검색하고 싶은 key값을 입력하세요 : "<<endl;
			cin >> scnode;
			sc = TreeSearch(Tree,temp, scnode);
			if (sc != Tree->nil)
				cout << "검색한 값 : (" << sc->key << "," << sc->value << sc->color<< ")"<<endl;
			else
				cout << "그 값은 존재하지 않습니다."<<endl;
			break;
		}
		case 7:
		{
			cout<<"가장 작은 노드의 값은 : ("<<TreeMinimum(Tree,temp)->key<<","<< TreeMinimum(Tree,temp)->value<< TreeMinimum(Tree, temp)->color << ")"<<endl;
			break;
		}
		case 8:
		{
			cout << "가장 큰 노드의 값은 : (" << TreeMaximum(Tree,temp)->key << "," << TreeMaximum(Tree,temp)->value << TreeMaximum(Tree, temp)->color << ")" << endl;
			break;
		}
		case 9:
		{
			node *front;
			front = TreeSuccessor(Tree,temp);
			cout << "루트 노드 값 : (" << Tree->root->key << ", " << Tree->root->value << ")" << endl;
			if (front != NULL)
				cout << "root 노드의 직후 노드의 값은 : (" << front->key << "," << front->value << front->color<<")" << endl;
			else
				cout << "root노드의 직후 노드 값이 존재하지 않습니다." << endl;
			break;
		}
		case 10:
		{
			node *back;
			back = TreePredecessor(Tree,temp);
			cout << "루트 노드 값 : (" << Tree->root->key << ", " << Tree->root->value << ")" << endl;
			if (back != NULL)
				cout << "root 노드의 직전 노드의 값은 : (" << back->key << "," << back->value << back->color<<")" << endl;
			else
				cout << "root노드의 직전 노드 값이 존재하지 않습니다." << endl;
			break;
		}
		case 11:
		{
			exit(1);
		}
		default:
		{
			cout << "메뉴에 있지 않습니다.";
			exit(1);
		}

		}
	}
	//cout << "(" << temp->key << " " << temp->value << ")";
}