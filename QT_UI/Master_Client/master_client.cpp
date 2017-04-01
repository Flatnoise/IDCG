#include "master_client.h"
#include "ui_master_client.h"

Master_Client::Master_Client(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::Master_Client)
{
    ui->setupUi(this);
}

Master_Client::~Master_Client()
{
    delete ui;
}
