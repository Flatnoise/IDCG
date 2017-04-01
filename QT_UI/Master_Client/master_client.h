#ifndef MASTER_CLIENT_H
#define MASTER_CLIENT_H

#include <QMainWindow>

namespace Ui {
class Master_Client;
}

class Master_Client : public QMainWindow
{
    Q_OBJECT

public:
    explicit Master_Client(QWidget *parent = 0);
    ~Master_Client();

private:
    Ui::Master_Client *ui;
};

#endif // MASTER_CLIENT_H
