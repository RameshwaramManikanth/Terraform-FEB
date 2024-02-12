resource "aws_vpc" "myvpc"{
    cidr_block=var.v_cidr
	tags=merge({Name="Vpc1"},var.v_tags)
}
resource "aws_subnet" "pubsn"{
    count=length(var.v_pubsn)
    cidr_block=element(var.v_pubsn,count.index)
	availability_zone=element(var.v_azs,count.index)
	vpc_id=aws_vpc.myvpc.id
	tags=merge({Name=join("-",["pubsn",count.index])},var.v_tags)
}
resource "aws_subnet" "pvtsn"{
    count=length(var.v_pvtsn)
    cidr_block=element(var.v_pvtsn,count.index)
	availability_zone=element(var.v_azs,count.index)
	vpc_id=aws_vpc.myvpc.id
	tags=merge({Name=join("-",["pvtsn",count.index])},var.v_tags)
}
resource "aws_internet_gateway" "igw"{
    vpc_id=aws_vpc.myvpc.id
	tags=merge({Name="IGW-myvpc"},var.v_tags)
}
resource "aws_route_table" "PubRT"{
    vpc_id=aws_vpc.myvpc.id
	route{
	    cidr_block="0.0.0.0/0"
		gateway_id=aws_internet_gateway.igw.id
	}
	tags=merge({Name="PubRT"},var.v_tags)
}
resource "aws_route_table_association" "pubRTass"{
    count=length(var.v_pubsn)
    subnet_id=aws_subnet.pubsn.*.id[count.index]
	route_table_id=aws_route_table.PubRT.id
}
resource "aws_eip" "myeip"{
    tags=merge({Name="myeip"},var.v_tags)
}
resource "aws_nat_gateway" "nat"{
    allocation_id=aws_eip.myeip.allocation_id
	subnet_id=aws_subnet.pubsn.*.id[0]
	tags=merge({Name="NAT-Vpc1"},var.v_tags)
}
resource "aws_route_table" "NATRT"{
    vpc_id=aws_vpc.myvpc.id
	route{
	    cidr_block="0.0.0.0/0"
		nat_gateway_id=aws_nat_gateway.nat.id
	}
	tags=merge({Name="NatRT"},var.v_tags)
}
resource "aws_route_table_association" "natRTass"{
    count=length(var.v_pvtsn)
    subnet_id=aws_subnet.pvtsn.*.id[count.index]
	route_table_id=aws_route_table.NATRT.id
}
Hello maniiiiii