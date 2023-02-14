#include "bis_gui.h"
#include "ui_bis_gui.h"

BIS_GUI::BIS_GUI(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::BIS_GUI)
{
    ui->setupUi(this);
}

BIS_GUI::~BIS_GUI()
{
    delete ui;
}
