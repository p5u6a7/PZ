from route import *
from loadOsm import LoadOsm

def routeToGpx(lat1, lon1, lat2, lon2):
    data = LoadOsm('cycle')

    node1 = data.findNode(lat1, lon1)
    node2 = data.findNode(lat2, lon2)

    router = Router(data)
    result, route = router.doRoute(node1, node2)

    count = 0
    node=[]
    for i in route:
        node.append(data.rnodes[i])
        '''node[0]=data.rnodes[i]'''
        '''node.append(data.rnodes[i])'''
        '''node[1]=data.rnodes[i]'''
        count = count + 1
        print node[0][0], node[0][1], count


if __name__ == "__main__":
        import sys
        print routeToGpx(float(52.9828), float(18.5729), float(53.0102), float(18.5946))